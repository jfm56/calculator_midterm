"""Contains calculator operations for history."""
class History:
    """Maintains the history of calculations performed."""

    _history = []

    @classmethod
    def add_entry(cls, operation, a, b, result):
        """Adds a calculation entry to history."""
        cls._history.append(f"{operation} {a} {b} = {result}")

    @classmethod
    def get_history(cls):
        """Returns the calculation history as a string."""
        return "\n".join(cls._history) if cls._history else "No calculations yet."

    @classmethod
    def get_last_entry(cls):
        """Returns the last calculation performed."""
        return cls._history[-1] if cls._history else "No history available."

    @classmethod
    def clear_history(cls):
        """Clears all stored history."""
        cls._history.clear()
