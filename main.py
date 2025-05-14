"""
Main script demonstrating the use of data validation and visualization.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Import our custom modules
from data_loader import CSVLoader, DataLoaderFactory
from validator import (
    NumericValidator, 
    DateValidator, 
    CategoricalValidator, 
    CompositeValidator, 
    ValidationResult
)
from visualizer import BarChart, LineChart, ScatterPlot, VisualizerFactory
from utils import DataUtility, Logger, ReportGenerator


def main():
    """
    Main function demonstrating the workflow of data validation and visualization.
    """
    # Set up logging
    logger = Logger("logs/validation.log")
    logger.info("Starting data validation process")
    
    # 1. Load the data
    logger.info("Loading data from CSV file")
    data_path = "data/sample_data.csv"
    loader = CSVLoader(data_path)
    raw_data = loader.load()
    
    print(f"Loaded data with {len(raw_data)} rows and {len(raw_data.columns)} columns")
    print("First few rows:")
    print(raw_data.head())
    
    # 2. Create validators
    logger.info("Setting up data validators")
    
    # Composite validator with multiple validation rules
    validator = CompositeValidator()
    
    # Add numeric validation for temperature and humidity
    validator.add_validator(
        NumericValidator(
            columns=["temperature", "humidity"], 
            min_value=0,  # Non-negative values
            max_value=100  # Reasonable upper limit
        )
    )
    
    # Add date validation
    validator.add_validator(
        DateValidator(
            column="date", 
            format="%Y-%m-%d",
            start_date="2022-01-01",  # Dates must be after 2022
            end_date=datetime.now().strftime("%Y-%m-%d")  # Dates must be before today
        )
    )
    
    # Add categorical validation for location
    validator.add_validator(
        CategoricalValidator(
            columns="location",
            allowed_values=["New York", "Los Angeles", "Chicago", "Houston", "Miami"]
        )
    )
    
    # 3. Validate the data
    logger.info("Validating data")
    validation_result = validator.validate(raw_data)
    
    if validation_result.is_valid:
        print("Data validation passed successfully!")
    else:
        print(f"Data validation found {len(validation_result.errors)} issues:")
        for error in validation_result.errors:
            print(f"  - {error}")
    
    # Get the valid data
    valid_data = validation_result.data
    print(f"\nAfter validation: {len(valid_data)} valid rows")
    
    # 4. Generate a validation report
    logger.info("Generating validation report")
    report_generator = ReportGenerator(valid_data, "reports")
    summary = report_generator.generate_summary()
    numeric_stats = report_generator.generate_numeric_stats()
    
    # Create a comprehensive report
    report = {
        "Data Summary": summary,
        "Numeric Statistics": numeric_stats,
        "Validation Errors": validation_result.errors,
        "Validation Status": "Passed" if validation_result.is_valid else "Failed"
    }
    
    # Save the report
    report_path = report_generator.save_report(report, "validation_report.txt")
    print(f"Validation report saved to: {report_path}")
    
    # 5. Visualize the data
    logger.info("Creating visualizations")
    
    # Example 1: Create a line chart of temperature over time
    print("\nCreating temperature line chart...")
    line_chart = LineChart(title="Temperature Over Time", marker='o')
    line_chart.plot(valid_data.sort_values('date'), x='date', y='temperature')
    line_chart.save("reports/temperature_chart.png")
    
    # Example 2: Create a bar chart of humidity by date
    print("Creating humidity bar chart...")
    bar_chart = BarChart(title="Average Humidity by Date")
    bar_chart.plot(valid_data, x='date', y='humidity')
    bar_chart.save("reports/humidity_chart.png")
    
    # Example 3: Create a scatter plot of temperature vs humidity
    print("Creating temperature vs humidity scatter plot...")
    scatter_plot = ScatterPlot(title="Temperature vs Humidity")
    scatter_plot.plot(valid_data, x='temperature', y='humidity', color='blue', size=50)
    scatter_plot.save("reports/temperature_humidity_scatter.png")
    
    # Example 4: Using the factory pattern to create visualizers
    print("Creating visualizations using factory pattern...")
    chart_types = ['bar', 'line', 'scatter', 'heatmap']
    
    for chart_type in chart_types:
        print(f"  - Creating {chart_type} chart")
        visualizer = VisualizerFactory.create_visualizer(
            chart_type, 
            title=f"{chart_type.capitalize()} Chart Example"
        )
        
        if chart_type == 'heatmap':
            # For heatmap, use the numeric columns correlation
            numeric_data = valid_data.select_dtypes(include=['number'])
            visualizer.plot(numeric_data, correlation=True)
        elif chart_type == 'scatter':
            visualizer.plot(valid_data, x='temperature', y='humidity')
        else:
            visualizer.plot(valid_data, x='date', y='temperature')
            
        visualizer.save(f"reports/{chart_type}_example.png")
    
    # 6. Using utility functions
    print("\nDemonstrating utility functions...")
    
    # Remove outliers from temperature
    print("Removing outliers from temperature data...")
    clean_data = DataUtility.remove_outliers(valid_data, 'temperature', method='zscore')
    print(f"After outlier removal: {len(clean_data)} rows")
    
    # Normalize temperature values
    print("Normalizing temperature data...")
    normalized_data = DataUtility.normalize_column(clean_data, 'temperature')
    print("First few rows with normalized temperature:")
    print(normalized_data[['date', 'temperature']].head())
    
    logger.info("Data validation and visualization process completed successfully")
    print("\nAll operations completed successfully. Check the reports folder for outputs.")


if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    try:
        main()
    except Exception as e:
        logger = Logger()
        logger.error(f"Error in main process: {str(e)}")
        print(f"An error occurred: {str(e)}")
