"""
Operation Mapping - Maps operation names to their respective classes.
"""

from operations.addition import Add
from operations.subtraction import Subtract
from operations.multiplication import Multiply
from operations.division import Divide
from operations.statistics import Mean, Median, StandardDeviation, Variance

# ✅ Dictionary mapping operation names to their corresponding functions
operation_mapping = {
    "add": Add().execute,
    "subtract": Subtract().execute,
    "multiply": Multiply().execute,
    "divide": Divide().execute,
    "mean": Mean().execute,
    "median": Median().execute,
    "std_dev": StandardDeviation().execute,
    "variance": Variance().execute,
}
