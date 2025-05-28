"""
Configuration utilities for Bharat AI Buddy application
"""
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Logger configuration
logger = logging.getLogger("bharat_buddy")

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Application configuration with defaults
class Config:
    # Security settings
    ENABLE_CODE_EXECUTION = os.getenv('ENABLE_CODE_EXECUTION', 'true').lower() == 'true'
    SANDBOX_CODE_EXECUTION = os.getenv('SANDBOX_CODE_EXECUTION', 'true').lower() == 'true'
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    MAX_HISTORY_LENGTH = int(os.getenv('MAX_HISTORY_LENGTH', 10))
    
# Global config instance
config = Config()

# Log the loading of the config
logger.info("config.py loaded.")

def get_agent_config():
    """
    Returns a dictionary with agent configuration settings
    """
    return {
        'sandbox_execution': config.SANDBOX_CODE_EXECUTION,
        'enable_code_execution': config.ENABLE_CODE_EXECUTION,
        'debug': config.DEBUG
    }
