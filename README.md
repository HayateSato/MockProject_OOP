# Data Validation for Visualization

This simple project demonstrates Object-Oriented Programming (OOP) principles in Python by implementing a data validation system for visualization purposes.

## Project Structure

- `main.py`: Entry point of the application
- `validator.py`: Contains the base Validator class and specialized validators
- `data_loader.py`: Handles loading data from various sources
- `visualizer.py`: Contains classes for data visualization
- `utils.py`: Utility functions and helper classes
- `data/`: Directory containing sample datasets
- `tests/`: Simple test cases

## How to Run

```bash
python main.py
```

## Learning Objectives

This project demonstrates key OOP concepts:

1. **Classes and Objects**: Building reusable components
2. **Inheritance**: Creating specialized validators from a base class
3. **Encapsulation**: Hiding implementation details
4. **Polymorphism**: Different validator types with consistent interfaces
5. **Composition**: Building complex objects from simpler ones

## Usage Example

```python
from data_loader import CSVLoader
from validator import NumericValidator, DateValidator
from visualizer import BarChart

# Load data
loader = CSVLoader("data/sample_data.csv")
data = loader.load()

# Validate data
numeric_validator = NumericValidator(columns=["temperature", "humidity"])
date_validator = DateValidator(column="date", format="%Y-%m-%d")

valid_data = numeric_validator.validate(data)
valid_data = date_validator.validate(valid_data)

# Visualize data
chart = BarChart(title="Temperature and Humidity")
chart.plot(valid_data, x="date", y=["temperature", "humidity"])
chart.show()
```
