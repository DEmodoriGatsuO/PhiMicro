import os
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the Replit environment"""
    
    logger.info("Starting environment setup...")
    
    # Create necessary directories
    os.makedirs("models", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Install required packages
    logger.info("Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        logger.info("Package installation completed")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during package installation: {e}")
        return False
    
    # Set environment variables
    os.environ["FLASK_APP"] = "app.py"
    
    # Download model
    logger.info("Downloading model...")
    try:
        from download_model import download_model
        download_model()
    except Exception as e:
        logger.error(f"Error during model download: {e}")
        return False
    
    logger.info("Setup completed!")
    return True

if __name__ == "__main__":
    if setup_environment():
        logger.info("Setup successful. You can start the application with `python app.py`.")
    else:
        logger.error("Setup failed. Please check the logs.")
        sys.exit(1)