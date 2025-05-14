"""
Data visualization module.
Demonstrates inheritance, polymorphism and interface implementation.
"""
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod


class Visualizer(ABC):
    """
    Abstract base class for data visualizers.
    Demonstrates abstract class definition.
    """
    def __init__(self, title=None, figsize=(10, 6)):
        self.title = title
        self.figsize = figsize
        self.fig = None
        self.ax = None
    
    @abstractmethod
    def plot(self, data, **kwargs):
        """
        Abstract method that must be implemented by subclasses.
        Should create the actual visualization.
        """
        pass
    
    def show(self):
        """
        Display the visualization.
        Common functionality shared by all visualizers.
        """
        if self.fig is not None:
            plt.show()
        else:
            print("Nothing to display, call plot() first")
    
    def save(self, filename, dpi=300):
        """
        Save the visualization to a file.
        Another common functionality.
        """
        if self.fig is not None:
            self.fig.savefig(filename, dpi=dpi)
            print(f"Visualization saved to {filename}")
        else:
            print("Nothing to save, call plot() first")
    
    def _create_figure(self):
        """
        Helper method to create a new figure.
        Demonstrates protected methods.
        """
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        if self.title:
            self.ax.set_title(self.title)


class BarChart(Visualizer):
    """
    Bar chart visualizer.
    Demonstrates inheritance and method overriding.
    """
    def __init__(self, title=None, figsize=(10, 6), orientation='vertical'):
        super().__init__(title, figsize)
        self.orientation = orientation
    
    def plot(self, data, x, y, color=None, **kwargs):
        """
        Create a bar chart.
        Implementation of the abstract method.
        """
        self._create_figure()
        
        # Handle multiple y values
        if isinstance(y, list):
            # Create a grouped bar chart
            bar_width = 0.8 / len(y)
            for i, col in enumerate(y):
                offset = (i - len(y) / 2 + 0.5) * bar_width
                positions = [pos + offset for pos in range(len(data))]
                if self.orientation == 'vertical':
                    self.ax.bar(positions, data[col], width=bar_width, label=col)
                else:
                    self.ax.barh(positions, data[col], height=bar_width, label=col)
            
            # Set x-axis labels
            if self.orientation == 'vertical':
                self.ax.set_xticks(range(len(data)))
                self.ax.set_xticklabels(data[x])
            else:
                self.ax.set_yticks(range(len(data)))
                self.ax.set_yticklabels(data[x])
            
            self.ax.legend()
        else:
            # Create a simple bar chart
            if self.orientation == 'vertical':
                self.ax.bar(data[x], data[y], color=color)
                plt.xticks(rotation=45 if len(data) > 5 else 0)
            else:
                self.ax.barh(data[x], data[y], color=color)
        
        # Set labels
        if self.orientation == 'vertical':
            self.ax.set_xlabel(x)
            self.ax.set_ylabel(y if isinstance(y, str) else "Value")
        else:
            self.ax.set_ylabel(x)
            self.ax.set_xlabel(y if isinstance(y, str) else "Value")
        
        self.fig.tight_layout()
        return self


class LineChart(Visualizer):
    """
    Line chart visualizer.
    Another example of inheritance and specialization.
    """
    def __init__(self, title=None, figsize=(10, 6), marker=None):
        super().__init__(title, figsize)
        self.marker = marker
    
    def plot(self, data, x, y, color=None, **kwargs):
        """
        Create a line chart.
        Implementation of the abstract method.
        """
        self._create_figure()
        
        # Handle multiple y values
        if isinstance(y, list):
            for col in y:
                self.ax.plot(data[x], data[col], marker=self.marker, label=col)
            self.ax.legend()
        else:
            self.ax.plot(data[x], data[y], marker=self.marker, color=color)
        
        # Set labels
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y if isinstance(y, str) else "Value")
        
        # Rotate x labels if there are many
        if len(data) > 5:
            plt.xticks(rotation=45)
        
        self.fig.tight_layout()
        return self


class ScatterPlot(Visualizer):
    """
    Scatter plot visualizer.
    Another example of inheritance.
    """
    def __init__(self, title=None, figsize=(10, 6), alpha=0.7):
        super().__init__(title, figsize)
        self.alpha = alpha
    
    def plot(self, data, x, y, color=None, size=None, **kwargs):
        """
        Create a scatter plot.
        Implementation of the abstract method.
        """
        self._create_figure()
        
        # Create scatter plot with optional size and color mapping
        scatter_kwargs = {"alpha": self.alpha}
        if size is not None:
            scatter_kwargs["s"] = data[size] * 20 if size in data.columns else size
        
        if color is not None and color in data.columns:
            scatter = self.ax.scatter(data[x], data[y], c=data[color], **scatter_kwargs)
            plt.colorbar(scatter, ax=self.ax, label=color)
        else:
            self.ax.scatter(data[x], data[y], color=color, **scatter_kwargs)
        
        # Set labels
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        
        self.fig.tight_layout()
        return self


class HeatMap(Visualizer):
    """
    Heat map visualizer.
    Demonstrates another visualization type.
    """
    def __init__(self, title=None, figsize=(10, 8), cmap="viridis"):
        super().__init__(title, figsize)
        self.cmap = cmap
    
    def plot(self, data, **kwargs):
        """
        Create a heat map of correlation matrix or pivot table.
        """
        self._create_figure()
        
        # If data is a DataFrame, compute correlation matrix by default
        if "correlation" in kwargs and kwargs["correlation"]:
            matrix = data.corr()
        else:
            matrix = data
        
        # Create heatmap
        sns.heatmap(matrix, annot=True, cmap=self.cmap, ax=self.ax)
        
        self.fig.tight_layout()
        return self


# Factory for creating appropriate visualizers
class VisualizerFactory:
    """
    Factory class to create visualizers.
    Demonstrates Factory design pattern.
    """
    @staticmethod
    def create_visualizer(chart_type, **kwargs):
        """
        Creates and returns a visualizer of the specified type.
        """
        if chart_type.lower() == 'bar':
            return BarChart(**kwargs)
        elif chart_type.lower() == 'line':
            return LineChart(**kwargs)
        elif chart_type.lower() == 'scatter':
            return ScatterPlot(**kwargs)
        elif chart_type.lower() == 'heatmap':
            return HeatMap(**kwargs)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
