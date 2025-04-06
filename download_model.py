import os
import sys
from huggingface_hub import hf_hub_download
from config import MODEL_CONFIG
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_model():
    """Download the model for PhiMicro from Hugging Face"""
    
    # Create model directory
    model_dir = os.path.dirname(MODEL_CONFIG['path'])
    os.makedirs(model_dir, exist_ok=True)
    
    # Skip if already exists
    if os.path.exists(MODEL_CONFIG['path']):
        logger.info(f"Model file already downloaded: {MODEL_CONFIG['path']}")
        return
    
    try:
        logger.info("Downloading model from Hugging Face...")
        
        # Download from HuggingFace Hub
        # Use quantized model to reduce size
        hf_hub_download(
            repo_id="TheBloke/phi-4-mini-instruct-GGUF", 
            filename="phi-4-mini-instruct.Q4_K_M.gguf",  # Quantized smaller model
            local_dir=model_dir,
            local_dir_use_symlinks=False,
            resume_download=True,  # Can resume if interrupted
        )
        
        # Adjust filename
        downloaded_path = os.path.join(model_dir, "phi-4-mini-instruct.Q4_K_M.gguf")
        if os.path.exists(downloaded_path) and downloaded_path != MODEL_CONFIG['path']:
            os.rename(downloaded_path, MODEL_CONFIG['path'])
            
        logger.info(f"Model download completed: {MODEL_CONFIG['path']}")
        
    except Exception as e:
        logger.error(f"Error during model download: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_model()