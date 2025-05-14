"""
Simple test cases for the data validation components.
"""
import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from data_loader import CSVLoader
from validator import NumericValidator, DateValidator, CategoricalValidator
from utils import DataUtility


class TestValidators(unittest.TestCase):
    """
    Test cases for validator classes.
    Demonstrates unit testing of OOP components.
    """
    def setUp(self):
        """Set up test data."""
        # Create a simple test dataframe
        self.test_data = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', 'not-a-date', '2023-01-04'],
            'temperature': [25.5, 26.8, 'invalid', 24.3],
            'humidity': [60, 65, 70, 58],
            'location': ['New York', 'Chicago', 'Boston', 'Miami']
        })
    
    def test_numeric_validator(self):
        """Test the NumericValidator class."""
        validator = NumericValidator(columns='temperature', min_value=0, max_value=50)
        result = validator.validate(self.test_data)
        
        # Check validation results
        self.assertFalse(result.is_valid)  # Should find an invalid value
        self.assertEqual(len(result.errors), 1)  # One error for 'invalid'
        self.assertEqual(len(result.data), 3)  # 3 valid rows after validation
        
        # Test with valid data only
        valid_data = pd.DataFrame({
            'temperature': [25.5, 26.8, 24.3]
        })
        valid_result = validator.validate(valid_data)
        self.assertTrue(valid_result.is_valid)
        self.assertEqual(len(valid_result.errors), 0)
    
    def test_date_validator(self):
        """Test the DateValidator class."""
        validator = DateValidator(column='date', format='%Y-%m-%d')
        result = validator.validate(self.test_data)
        
        # Check validation results
        self.assertFalse(result.is_valid)  # Should find an invalid date
        self.assertEqual(len(result.errors), 1)  # One error for 'not-a-date'
        self.assertEqual(len(result.data), 3)  # 3 valid rows after validation
    
    def test_categorical_validator(self):
        """Test the CategoricalValidator class."""
        allowed_cities = ['New York', 'Chicago', 'Miami', 'Los Angeles', 'Houston']
        validator = CategoricalValidator(columns='location', allowed_values=allowed_cities)
        result = validator.validate(self.test_data)
        
        # Check validation results
        self.assertFalse(result.is_valid)  # Should find Boston is not allowed
        self.assertEqual(len(result.errors), 1)  # One error
        # Note: CategoricalValidator doesn't remove invalid rows by default
        self.assertEqual(len(result.data), 4)


class TestUtilities(unittest.TestCase):
    """
    Test cases for utility functions.
    """
    def setUp(self):
        """Set up test data."""
        # Create a simple test dataframe
        self.test_data = pd.DataFrame({
            'values': [10, 15, 12, 100, 13, 11, np.nan, 14]
        })
    
    def test_remove_outliers(self):
        """Test removing outliers."""
        # Using Z-score method
        result = DataUtility.remove_outliers(self.test_data, 'values', method='zscore')
        # 100 should be removed as an outlier, and np.nan is also removed
        self.assertEqual(len(result), 6)
        self.assertNotIn(100, result['values'].values)
        
        # Using IQR method
        result_iqr = DataUtility.remove_outliers(self.test_data, 'values', method='iqr')
        self.assertEqual(len(result_iqr), 6)
        self.assertNotIn(100, result_iqr['values'].values)
    
    def test_impute_missing_values(self):
        """Test imputing missing values."""
        # Get the mean of values
        mean_value = self.test_data['values'].mean()
        
        # Test imputing with mean
        result = DataUtility.impute_missing_values(self.test_data, 'values', method='mean')
        self.assertEqual(len(result), 8)  # All rows preserved
        self.assertFalse(result['values'].isna().any())  # No NaN values
        self.assertEqual(result['values'].iloc[6], mean_value)  # NaN replaced with mean
        
        # Test imputing with constant
        const_value = 999
        result_const = DataUtility.impute_missing_values(self.test_data, 'values', method=const_value)
        self.assertEqual(result_const['values'].iloc[6], const_value)  # NaN replaced with constant
    
    def test_normalize_column(self):
        """Test normalizing columns."""
        # Fill NaN value for this test
        test_data_filled = self.test_data.copy()
        test_data_filled['values'] = test_data_filled['values'].fillna(0)
        
        # Test min-max normalization
        result = DataUtility.normalize_column(test_data_filled, 'values', method='minmax')
        self.assertEqual(result['values'].min(), 0)  # Min should be 0
        self.assertEqual(result['values'].max(), 1)  # Max should be 1
        
        # Test z-score normalization
        result_z = DataUtility.normalize_column(test_data_filled, 'values', method='zscore')
        self.assertAlmostEqual(result_z['values'].mean(), 0, delta=1e-10)  # Mean should be close to 0
        self.assertAlmostEqual(result_z['values'].std(), 1, delta=1e-10)  # Std should be close to 1


if __name__ == '__main__':
    unittest.main()
