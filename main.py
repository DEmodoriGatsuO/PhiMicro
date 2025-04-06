import os
import sys
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/app.log")
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    
    # Check model directory
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)
        logger.info(f"Created model directory: {model_dir}")
    
    # Check if model file exists
    from config import MODEL_CONFIG
    if not os.path.exists(MODEL_CONFIG['path']):
        logger.info("Model not yet downloaded. Starting download...")
        from download_model import download_model
        download_model()
    
    # Start application
    logger.info("Starting application...")
    os.environ["FLASK_APP"] = "app.py"
    
    # Adjust port according to Replit settings
    from app import app, APP_CONFIG
    port = int(os.environ.get("PORT", APP_CONFIG["port"]))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error during application execution: {e}")
        sys.exit(1)