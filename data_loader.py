"""
Data loading module for different data sources.
Demonstrates OOP concepts: abstraction, inheritance, and encapsulation.
"""
import csv
import json
import pandas as pd
from abc import ABC, abstractmethod


class DataLoader(ABC):
    """
    Abstract base class for data loaders.
    Demonstrates the use of abstract classes in Python.
    """
    def __init__(self, source_path):
        self.source_path = source_path
        
    @abstractmethod
    def load(self):
        """
        Abstract method that must be implemented by subclasses.
        Returns a pandas DataFrame with the loaded data.
        """
        pass
    
    def preview(self, rows=5):
        """
        Preview the data.
        Demonstrates method implementation in abstract classes.
        """
        data = self.load()
        return data.head(rows)


class CSVLoader(DataLoader):
    """
    Loader for CSV files.
    Demonstrates inheritance from an abstract base class.
    """
    def __init__(self, source_path, delimiter=','):
        super().__init__(source_path)  # Call to parent constructor
        self.delimiter = delimiter
        
    def load(self):
        """
        Implementation of the abstract method from the parent class.
        Demonstrates method overriding.
        """
        try:
            return pd.read_csv(self.source_path, delimiter=self.delimiter)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()
        
    def load_raw(self):
        """
        Additional method specific to CSVLoader.
        Demonstrates extending functionality in subclasses.
        """
        with open(self.source_path, 'r') as file:
            reader = csv.reader(file, delimiter=self.delimiter)
            data = list(reader)
        return data


class JSONLoader(DataLoader):
    """
    Loader for JSON files.
    Another example of inheritance from the base class.
    """
    def load(self):
        """
        Implementation of the abstract method for JSON files.
        """
        try:
            return pd.read_json(self.source_path)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return pd.DataFrame()


class ExcelLoader(DataLoader):
    """
    Loader for Excel files.
    Another implementation of the DataLoader interface.
    """
    def __init__(self, source_path, sheet_name=0):
        super().__init__(source_path)
        self.sheet_name = sheet_name
        
    def load(self):
        """
        Implementation of the abstract method for Excel files.
        """
        try:
            return pd.read_excel(self.source_path, sheet_name=self.sheet_name)
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return pd.DataFrame()


# Factory pattern implementation for creating appropriate loaders
class DataLoaderFactory:
    """
    Factory class to create appropriate data loaders.
    Demonstrates the Factory design pattern.
    """
    @staticmethod
    def create_loader(file_path):
        """
        Creates the appropriate loader based on file extension.
        """
        if file_path.endswith('.csv'):
            return CSVLoader(file_path)
        elif file_path.endswith('.json'):
            return JSONLoader(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return ExcelLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
