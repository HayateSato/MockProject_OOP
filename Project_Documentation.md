# MockProject_OOP: Data Validation and Visualization Framework

## Project Overview

This project demonstrates Object-Oriented Programming (OOP) principles in Python through a comprehensive data validation and visualization framework. The application provides a structured approach to loading, validating, and visualizing data using various design patterns and OOP concepts including inheritance, polymorphism, encapsulation, abstraction, and composition.

## Project Structure

```
MockProject_OOP/
│
├── data/                    # Directory for sample datasets
│   └── sample_data.csv      # Sample CSV data for testing
│
├── tests/                   # Test cases
│   └── test_validators.py   # Unit tests for validators and utilities
│
├── main.py                  # Entry point and workflow demonstration
├── data_loader.py           # Data loading classes for different file types
├── validator.py             # Data validation framework
├── visualizer.py            # Data visualization components
├── utils.py                 # Utility functions and helper classes
└── README.md                # Project overview and usage instructions
```

## Core Modules

### 1. data_loader.py

This module handles loading data from various sources using the Abstract Factory pattern.

#### Key Classes:

- **DataLoader (ABC)**: Abstract base class that defines the interface for all data loaders
  - Defines abstract `load()` method
  - Provides a concrete implementation of `preview()` method

- **CSVLoader**: Loads data from CSV files
  - Implements `load()` method for CSV files
  - Adds a specialized `load_raw()` method for raw CSV access

- **JSONLoader**: Loads data from JSON files
  - Implements `load()` method for JSON files

- **ExcelLoader**: Loads data from Excel files
  - Implements `load()` method for Excel files

- **DataLoaderFactory**: Factory class that creates appropriate loaders based on file extension
  - Implements the Factory design pattern for dynamic object creation

### 2. validator.py

This module provides a robust framework for data validation using the Composite design pattern.

#### Key Classes:

- **ValidationError**: Custom exception for validation errors

- **ValidationResult**: Container class for validation results
  - Encapsulates validation status, validated data, and error messages
  - Demonstrates proper encapsulation with properties

- **Validator (ABC)**: Abstract base class for all validators
  - Defines the Template Method pattern with `validate()` and abstract `_validate_data()`
  - Provides common functionality for target column handling

- **NumericValidator**: Validates numeric data
  - Checks for valid numbers and applies min/max constraints
  - Specializes the base Validator class

- **DateValidator**: Validates date fields
  - Checks for valid dates and applies date range constraints
  - Specializes the base Validator class

- **CategoricalValidator**: Validates categorical data
  - Ensures values are within an allowed set of values
  - Specializes the base Validator class

- **CompositeValidator**: Combines multiple validators
  - Implements the Composite design pattern
  - Allows method chaining through fluent interface

### 3. visualizer.py

This module handles data visualization using Matplotlib and Seaborn with the Strategy pattern.

#### Key Classes:

- **Visualizer (ABC)**: Abstract base class for all visualizers
  - Defines common interface with abstract `plot()` method
  - Provides common functionality for showing and saving visualizations

- **BarChart**: Creates bar charts
  - Handles both simple and grouped bar charts
  - Supports both vertical and horizontal orientations

- **LineChart**: Creates line charts
  - Supports single or multiple line plots
  - Allows customization of markers

- **ScatterPlot**: Creates scatter plots
  - Supports color mapping and size variation
  - Handles transparency through alpha parameter

- **HeatMap**: Creates heat maps
  - Visualizes correlation matrices or custom data
  - Customizable color mapping

- **VisualizerFactory**: Factory class that creates visualizers
  - Implements the Factory design pattern for visualization strategies

### 4. utils.py

This module provides utility functions and helper classes to support the main components.

#### Key Classes:

- **DataUtility**: Static utility methods for data manipulation
  - Demonstrates the Utility Class pattern
  - Provides methods for outlier removal, missing value imputation, and normalization

- **Logger**: Logging utility with singleton pattern
  - Implements Singleton pattern to ensure a single logger instance
  - Provides unified logging to console and file

- **ReportGenerator**: Generates data reports
  - Demonstrates composition with data objects
  - Creates summary statistics and formatted reports

### 5. main.py

The entry point of the application that demonstrates the complete workflow.

#### Key Functions:

- **main()**: Orchestrates the entire process
  1. Loads data from a CSV file
  2. Creates a composite validator with multiple validation rules
  3. Validates the data and handles validation errors
  4. Generates a validation report
  5. Creates various visualizations to display the data
  6. Demonstrates utility functions for data cleaning

## OOP Concepts Demonstrated

### 1. Inheritance

- **Class Hierarchies**: DataLoader → CSVLoader, JSONLoader, ExcelLoader
- **Method Overriding**: Each child class implements its version of `load()`
- **Abstract Base Classes**: DataLoader, Validator, and Visualizer classes define interfaces

### 2. Polymorphism

- **Common Interfaces**: All validators share the `validate()` method
- **Method Overriding**: Different implementations of `_validate_data()` and `plot()`
- **Duck Typing**: Objects used interchangeably based on interface, not type

### 3. Encapsulation

- **Private Methods**: Methods prefixed with underscore (e.g., `_validate_data`)
- **Properties**: ValidationResult uses properties to control access
- **Data Hiding**: Internal state is protected from direct manipulation

### 4. Abstraction

- **Abstract Base Classes**: DataLoader, Validator, and Visualizer define contracts
- **Interface Separation**: Clear boundaries between components
- **Implementation Hiding**: Details hidden behind clean interfaces

### 5. Composition

- **Object Composition**: CompositeValidator contains multiple Validator objects
- **Has-A Relationships**: ReportGenerator uses Logger rather than inheriting from it
- **Delegation**: CompositeValidator delegates to contained validators

### 6. Design Patterns

- **Factory Pattern**: DataLoaderFactory and VisualizerFactory
- **Composite Pattern**: CompositeValidator
- **Strategy Pattern**: Different Validator and Visualizer implementations
- **Template Method**: Validator.validate() uses template method pattern
- **Singleton**: Logger implements singleton pattern

## Sample Data

The project includes a sample CSV file (`sample_data.csv`) with the following structure:
- **date**: Date values in YYYY-MM-DD format (some invalid)
- **temperature**: Temperature readings (some invalid)
- **humidity**: Humidity percentage
- **precipitation**: Precipitation amount
- **location**: City names

## Testing

The project includes unit tests in the `tests/` directory:

- **TestValidators**: Tests for the validator classes
  - Tests NumericValidator, DateValidator, and CategoricalValidator
  - Verifies validation results and error handling

- **TestUtilities**: Tests for utility functions
  - Tests outlier removal, missing value imputation, and normalization
  - Verifies function behavior with various parameters

## Usage Example

```python
# Load data
loader = CSVLoader("data/sample_data.csv")
data = loader.load()

# Create validators
validator = CompositeValidator()
validator.add_validator(NumericValidator(columns=["temperature", "humidity"]))
validator.add_validator(DateValidator(column="date", format="%Y-%m-%d"))

# Validate data
result = validator.validate(data)

# Create visualization
chart = BarChart(title="Temperature by Date")
chart.plot(result.data, x="date", y="temperature")
chart.save("temperature_chart.png")
```

## Learning Objectives

This project serves as a comprehensive example of Object-Oriented Programming and demonstrates:

1. Separation of concerns through modular design
2. Creating reusable components through abstraction
3. Implementing design patterns to solve common problems
4. Writing maintainable and extensible code
5. Applying OOP principles to a practical data processing workflow

## Future Enhancements

Potential areas for expansion:
1. Adding more data sources (databases, APIs, etc.)
2. Implementing additional validators for more complex data types
3. Expanding visualization options with interactive charts
4. Adding more sophisticated data processing utilities
5. Implementing a graphical user interface (GUI)
