"""
Main application entry point for Bharat AI Buddy
"""
import os
import sys
import logging
from ui import build_ui
from config import config

# Configure logging
def setup_logging():
    """Set up logging for the application"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "bharat_buddy.log")
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("bharat_buddy")
    logger.info("Logging initialized.")
    return logger

def initialize_app():
    """Initialize application dependencies and environment"""
    logger = setup_logging()
    logger.info("Initializing application dependencies and environment.")
    
    # Ensure required folders exist
    os.makedirs("tmp", exist_ok=True)
    
    # Import standard modules
    try:
        # Import standard modules directly
        import app_logic
        import agent_tools
        
        logger.info("Successfully loaded standard modules")
    except ImportError as e:
        logger.error(f"Failed to import standard modules: {e}")
    
    # Log initialization
    if config.DEBUG:
        logger.debug("Debug mode enabled")
        logger.debug(f"Using model API URL: {config.VLLM_API_URL}")
        logger.debug(f"Code execution enabled: {config.ENABLE_CODE_EXECUTION}")
        logger.debug(f"Sandbox execution enabled: {config.SANDBOX_CODE_EXECUTION}")
    
    logger.info("Initialization complete.")
    return logger

def main():
    # Initialize the application
    logger = initialize_app()
    logger.info("Starting main application flow.")
    try:
        # Build and launch the UI
        demo = build_ui()
        logger.info("UI built successfully. Launching app...")
        demo.launch(share=True, debug=config.DEBUG)
        logger.info("App launched.")
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        print(f"Error: Failed to start Bharat AI Buddy. See logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
