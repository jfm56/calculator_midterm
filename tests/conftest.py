"""Test configuration and shared fixtures for the calculator tests."""
import pytest
from history.history import History

@pytest.fixture(scope="function")
def setup_and_teardown():
    """Resets history before and after tests."""
    History.clear_history()
    yield
    History.clear_history()

@pytest.fixture(scope="function")
def monkeypatch_input(monkeypatch):
    """Helper to patch input for user input prompts."""
    def mock_input(prompt):
        if "remove" in prompt:
            return "1"
        return "exit"
    monkeypatch.setattr("builtins.input", mock_input)
