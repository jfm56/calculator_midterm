"""
Statistical Operations for the Calculator.
"""

from decimal import Decimal, ROUND_HALF_UP
import statistics
from operations.operation_base import Operation


class Mean(Operation):
    """Computes the mean (average) of a list of numbers."""

    @staticmethod
    def execute(*args) -> Decimal:
        """Returns the mean of the given numbers."""
        numbers = [Decimal(arg) for arg in args]
        return Decimal(statistics.mean(numbers)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class Median(Operation):
    """Computes the median of a list of numbers."""

    @staticmethod
    def execute(*args) -> Decimal:
        """Returns the median of the given numbers."""
        numbers = [Decimal(arg) for arg in args]
        result = statistics.median(numbers)
        return Decimal(str(result)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class StandardDeviation(Operation):
    """Computes the standard deviation of a list of numbers."""

    @staticmethod
    def execute(*args) -> Decimal:
        """Returns the standard deviation of the given numbers."""
        numbers = [Decimal(arg) for arg in args]
        return Decimal(statistics.stdev(numbers)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class Variance(Operation):
    """Computes the variance of a list of numbers."""

    @staticmethod
    def execute(*args) -> Decimal:
        """Returns the variance of the given numbers."""
        numbers = [Decimal(arg) for arg in args]
        if len(numbers) == 1:
            return Decimal(0)  # Avoids StatisticsError for single values
        result = statistics.variance(numbers)
        return Decimal(str(result)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
