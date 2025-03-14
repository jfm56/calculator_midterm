"""Tests for `log_config.py` logging behavior."""
import logging
import pytest
from config.log_config import logger

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    """Ensure log capture is set to DEBUG for all tests."""
    logger.propagate = True  # ✅ Ensure logs are captured by caplog
    caplog.set_level(logging.DEBUG, logger=logger.name)

def test_debug_logging(caplog):
    """Test to ensure debug messages are logged correctly."""
    logger.debug("Test debug message")

    # ✅ Use `caplog.records` to check both message and log level
    assert any(record.levelno == logging.DEBUG and "Test debug message" in record.message for record in caplog.records), \
        "⚠️ Expected debug message not found in logs"

def test_info_logging(caplog):
    """Test to ensure info messages are logged correctly."""
    logger.info("Test info message")

    assert any(record.levelno == logging.INFO and "Test info message" in record.message for record in caplog.records), \
        "⚠️ Expected info message not found in logs"

def test_error_logging(caplog):
    """Test to ensure error messages are logged correctly."""
    logger.error("Test error message")

    assert any(record.levelno == logging.ERROR and "Test error message" in record.message for record in caplog.records), \
        "⚠️ Expected error message not found in logs"
