"""
Utility functions and classes for data validation and visualization.
Demonstrates encapsulation and helper classes.
"""
import pandas as pd
import numpy as np
import os
import logging


class DataUtility:
    """
    Utility class for data manipulation.
    Demonstrates static methods and utility class pattern.
    """
    @staticmethod
    def remove_outliers(data, column, method='zscore', threshold=3):
        """
        Remove outliers from a DataFrame.
        
        Parameters:
        - data: pandas DataFrame
        - column: column name to check for outliers
        - method: 'zscore' or 'iqr'
        - threshold: threshold for outlier detection
        
        Returns: DataFrame with outliers removed
        """
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in data")
        
        df_copy = data.copy()
        
        if method == 'zscore':
            # Z-score method
            z_scores = np.abs((df_copy[column] - df_copy[column].mean()) / df_copy[column].std())
            outliers = z_scores > threshold
            return df_copy[~outliers]
        
        elif method == 'iqr':
            # IQR method
            Q1 = df_copy[column].quantile(0.25)
            Q3 = df_copy[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            return df_copy[(df_copy[column] >= lower_bound) & (df_copy[column] <= upper_bound)]
        
        else:
            raise ValueError(f"Unsupported outlier removal method: {method}")
    
    @staticmethod
    def impute_missing_values(data, column, method='mean'):
        """
        Impute missing values in a DataFrame.
        
        Parameters:
        - data: pandas DataFrame
        - column: column name to impute
        - method: 'mean', 'median', 'mode', or a constant value
        
        Returns: DataFrame with imputed values
        """
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in data")
        
        df_copy = data.copy()
        missing_mask = df_copy[column].isna()
        
        if not any(missing_mask):
            return df_copy  # No missing values
        
        if method == 'mean':
            df_copy.loc[missing_mask, column] = df_copy[column].mean()
        elif method == 'median':
            df_copy.loc[missing_mask, column] = df_copy[column].median()
        elif method == 'mode':
            df_copy.loc[missing_mask, column] = df_copy[column].mode()[0]
        else:
            # Assume method is a constant value
            df_copy.loc[missing_mask, column] = method
        
        return df_copy
    
    @staticmethod
    def normalize_column(data, column, method='minmax'):
        """
        Normalize values in a column.
        
        Parameters:
        - data: pandas DataFrame
        - column: column name to normalize
        - method: 'minmax' or 'zscore'
        
        Returns: DataFrame with normalized column
        """
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in data")
        
        df_copy = data.copy()
        
        if method == 'minmax':
            min_val = df_copy[column].min()
            max_val = df_copy[column].max()
            if max_val > min_val:
                df_copy[column] = (df_copy[column] - min_val) / (max_val - min_val)
        
        elif method == 'zscore':
            mean = df_copy[column].mean()
            std = df_copy[column].std()
            if std > 0:
                df_copy[column] = (df_copy[column] - mean) / std
        
        else:
            raise ValueError(f"Unsupported normalization method: {method}")
        
        return df_copy


class Logger:
    """
    Simple logging utility.
    Demonstrates another utility class and a singleton pattern.
    """
    _instance = None
    
    def __new__(cls, log_file=None, level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._configure_logger(log_file, level)
        return cls._instance
    
    def _configure_logger(self, log_file, level):
        """Configure the logger with handlers."""
        self.logger = logging.getLogger("DataValidationLogger")
        self.logger.setLevel(level)
        
        # Remove existing handlers if any
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Add file handler if log_file is provided
        if log_file:
            # Ensure directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
    
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)


class ReportGenerator:
    """
    Generate reports on data quality.
    Demonstrates another utility class with composition.
    """
    def __init__(self, data, output_dir=None):
        self.data = data
        self.output_dir = output_dir
        self.logger = Logger().logger
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_summary(self):
        """
        Generate a basic summary of the data.
        """
        summary = {
            "row_count": len(self.data),
            "column_count": len(self.data.columns),
            "columns": self.data.columns.tolist(),
            "missing_values": self.data.isna().sum().to_dict(),
            "numeric_columns": self.data.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": self.data.select_dtypes(include=["object"]).columns.tolist(),
            "datetime_columns": self.data.select_dtypes(include=["datetime"]).columns.tolist()
        }
        
        self.logger.info(f"Generated data summary: {len(self.data)} rows, {len(self.data.columns)} columns")
        return summary
    
    def generate_numeric_stats(self, columns=None):
        """
        Generate statistics for numeric columns.
        """
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        numeric_stats = {}
        for col in columns:
            if col in self.data.columns and pd.api.types.is_numeric_dtype(self.data[col]):
                stats = {
                    "min": self.data[col].min(),
                    "max": self.data[col].max(),
                    "mean": self.data[col].mean(),
                    "median": self.data[col].median(),
                    "std": self.data[col].std(),
                    "missing": self.data[col].isna().sum(),
                    "zeros": (self.data[col] == 0).sum(),
                    "negatives": (self.data[col] < 0).sum()
                }
                numeric_stats[col] = stats
            
        return numeric_stats
    
    def save_report(self, report, filename="data_report.txt"):
        """
        Save a report to a file.
        """
        if self.output_dir:
            filepath = os.path.join(self.output_dir, filename)
        else:
            filepath = filename
        
        with open(filepath, 'w') as f:
            f.write("Data Validation Report\n")
            f.write("=====================\n\n")
            
            for section, content in report.items():
                f.write(f"{section.upper()}\n")
                f.write("-" * len(section) + "\n")
                
                if isinstance(content, dict):
                    for key, value in content.items():
                        f.write(f"{key}: {value}\n")
                elif isinstance(content, list):
                    for item in content:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{content}\n")
                
                f.write("\n")
        
        self.logger.info(f"Report saved to {filepath}")
        return filepath
