"""
Data validation module.
Demonstrates inheritance, polymorphism, and encapsulation principles.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod


class ValidationError(Exception):
    """
    Custom exception for validation errors.
    Demonstrates creating custom exceptions.
    """
    pass


class ValidationResult:
    """
    Class to hold validation results.
    Demonstrates encapsulation and class composition.
    """
    def __init__(self, is_valid, data, errors=None):
        self._is_valid = is_valid
        self._data = data
        self._errors = errors if errors else []
        
    @property
    def is_valid(self):
        """Get validation status."""
        return self._is_valid
    
    @property
    def data(self):
        """Get the validated data."""
        return self._data
    
    @property
    def errors(self):
        """Get validation errors."""
        return self._errors
    
    def __str__(self):
        """String representation of validation result."""
        if self._is_valid:
            return f"Validation successful: {len(self._data)} valid records"
        else:
            return f"Validation failed with {len(self._errors)} errors"


class Validator(ABC):
    """
    Abstract base class for data validators.
    Demonstrates abstract class definition.
    """
    def __init__(self, columns=None):
        self.columns = columns
    
    @abstractmethod
    def _validate_data(self, data):
        """
        Abstract method that specific validators must implement.
        Should return a tuple of (valid_data, errors).
        """
        pass
    
    def validate(self, data):
        """
        Validate the data and return a ValidationResult.
        Template method pattern that uses the abstract _validate_data method.
        """
        valid_data, errors = self._validate_data(data)
        return ValidationResult(len(errors) == 0, valid_data, errors)
    
    def _get_target_columns(self, data):
        """
        Helper method to get columns to validate.
        Demonstrates protected methods and encapsulation.
        """
        if self.columns is None:
            return data.columns.tolist()
        elif isinstance(self.columns, list):
            return self.columns
        else:
            return [self.columns]


class NumericValidator(Validator):
    """
    Validator for numeric data.
    Demonstrates inheritance and method overriding.
    """
    def __init__(self, columns=None, min_value=None, max_value=None):
        super().__init__(columns)
        self.min_value = min_value
        self.max_value = max_value
    
    def _validate_data(self, data):
        """
        Implementation of the abstract method for numeric validation.
        Demonstrates method overriding.
        """
        errors = []
        df_copy = data.copy()
        
        for column in self._get_target_columns(data):
            if column not in df_copy.columns:
                errors.append(f"Column '{column}' not found in data")
                continue
                
            # Convert to numeric, coerce errors to NaN
            df_copy[column] = pd.to_numeric(df_copy[column], errors='coerce')
            
            # Find rows with NaN (conversion failed)
            invalid_rows = df_copy[df_copy[column].isna()].index.tolist()
            
            for row in invalid_rows:
                errors.append(f"Row {row}: '{data.loc[row, column]}' is not a valid number in column '{column}'")
            
            # Check min/max constraints if specified
            if self.min_value is not None:
                min_invalid = df_copy[(~df_copy[column].isna()) & (df_copy[column] < self.min_value)].index.tolist()
                for row in min_invalid:
                    errors.append(f"Row {row}: Value {df_copy.loc[row, column]} is less than minimum {self.min_value} in column '{column}'")
            
            if self.max_value is not None:
                max_invalid = df_copy[(~df_copy[column].isna()) & (df_copy[column] > self.max_value)].index.tolist()
                for row in max_invalid:
                    errors.append(f"Row {row}: Value {df_copy.loc[row, column]} is greater than maximum {self.max_value} in column '{column}'")
        
        # Remove rows with conversion errors
        valid_data = df_copy.dropna(subset=self._get_target_columns(data))
        
        return valid_data, errors


class DateValidator(Validator):
    """
    Validator for date fields.
    Another example of inheritance and specialization.
    """
    def __init__(self, column, format="%Y-%m-%d", start_date=None, end_date=None):
        super().__init__(column)  # column is a single string in this case
        self.format = format
        self.start_date = start_date
        self.end_date = end_date
    
    def _validate_data(self, data):
        """
        Implementation of the abstract method for date validation.
        """
        errors = []
        df_copy = data.copy()
        column = self._get_target_columns(data)[0]  # We expect a single column
        
        if column not in df_copy.columns:
            errors.append(f"Column '{column}' not found in data")
            return df_copy, errors
        
        # Function to validate dates
        def parse_date(value):
            try:
                return pd.to_datetime(value, format=self.format)
            except:
                return pd.NaT
        
        # Convert to datetime
        df_copy[column] = df_copy[column].apply(parse_date)
        
        # Find invalid dates
        invalid_rows = df_copy[df_copy[column].isna()].index.tolist()
        for row in invalid_rows:
            errors.append(f"Row {row}: '{data.loc[row, column]}' is not a valid date in format '{self.format}'")
        
        # Check date range if specified
        if self.start_date is not None:
            start = pd.to_datetime(self.start_date, format=self.format)
            before_start = df_copy[(~df_copy[column].isna()) & (df_copy[column] < start)].index.tolist()
            for row in before_start:
                errors.append(f"Row {row}: Date {df_copy.loc[row, column].strftime(self.format)} is before start date {self.start_date}")
        
        if self.end_date is not None:
            end = pd.to_datetime(self.end_date, format=self.format)
            after_end = df_copy[(~df_copy[column].isna()) & (df_copy[column] > end)].index.tolist()
            for row in after_end:
                errors.append(f"Row {row}: Date {df_copy.loc[row, column].strftime(self.format)} is after end date {self.end_date}")
        
        # Remove rows with invalid dates
        valid_data = df_copy.dropna(subset=[column])
        
        return valid_data, errors


class CategoricalValidator(Validator):
    """
    Validator for categorical data.
    Ensures values are within an allowed set.
    """
    def __init__(self, columns=None, allowed_values=None, case_sensitive=True):
        super().__init__(columns)
        self.allowed_values = allowed_values if allowed_values else []
        self.case_sensitive = case_sensitive
    
    def _validate_data(self, data):
        """
        Implementation of the abstract method for categorical validation.
        """
        errors = []
        df_copy = data.copy()
        
        for column in self._get_target_columns(data):
            if column not in df_copy.columns:
                errors.append(f"Column '{column}' not found in data")
                continue
            
            # Create comparison sets based on case sensitivity
            if not self.case_sensitive and all(isinstance(val, str) for val in self.allowed_values):
                allowed = {val.lower() for val in self.allowed_values}
                check_value = lambda x: str(x).lower() in allowed if pd.notna(x) else False
            else:
                allowed = set(self.allowed_values)
                check_value = lambda x: x in allowed if pd.notna(x) else False
            
            # Find invalid values
            for idx, value in df_copy[column].items():
                if not check_value(value):
                    errors.append(f"Row {idx}: Value '{value}' in column '{column}' is not in allowed values: {self.allowed_values}")
        
        # Return original data; we don't remove invalid rows by default for categorical validation
        # but we could implement a drop_invalid flag if needed
        return df_copy, errors


class CompositeValidator(Validator):
    """
    Composite validator that combines multiple validators.
    Demonstrates the Composite design pattern.
    """
    def __init__(self):
        super().__init__()
        self.validators = []
    
    def add_validator(self, validator):
        """Add a validator to the composite."""
        self.validators.append(validator)
        return self  # For method chaining
    
    def _validate_data(self, data):
        """
        Run all validators in sequence.
        """
        current_data = data.copy()
        all_errors = []
        
        for validator in self.validators:
            result = validator.validate(current_data)
            all_errors.extend(result.errors)
            current_data = result.data
        
        return current_data, all_errors
