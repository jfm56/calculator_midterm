"""
Operation Mapping - Maps operation names to their respective classes.
"""

from operations.addition import Add
from operations.subtraction import Subtract
from operations.multiplication import Multiply
from operations.division import Divide
from operations.statistics import Mean, Median, StandardDeviation, Variance

# ✅ Dictionary mapping operation names to their corresponding classes
operation_mapping = {
    "add": Add,
    "subtract": Subtract,
    "multiply": Multiply,
    "divide": Divide,
    "mean": Mean,
    "median": Median,
    "std_dev": StandardDeviation,
    "variance": Variance,
}
