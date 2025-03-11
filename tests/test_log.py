"""Tests for `log_config.py` logging behavior."""

import pytest
import logging
from config.log_config import logger

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    """Ensure log capture is set to DEBUG for all tests."""
    caplog.set_level(logging.DEBUG, logger=logger.name)

def test_debug_logging(caplog):
    """Test to ensure debug messages are logged correctly."""
    logger.debug("Test debug message")
    assert "Test debug message" in caplog.text

def test_info_logging(caplog):
    """Test to ensure info messages are logged correctly."""
    logger.info("Test info message")
    assert "Test info message" in caplog.text

def test_error_logging(caplog):
    """Test to ensure error messages are logged correctly."""
    logger.error("Test error message")
    assert "Test error message" in caplog.text
