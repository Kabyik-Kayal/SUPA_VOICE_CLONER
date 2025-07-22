import argparse
import os
import sys
from TTS.api import TTS
from TTS.utils.manage import ModelManager
from config.paths_config import MODEL_DIR
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

def download_pretrained_model(accept_tos=False):
    """
    Downloads the pretrained TTS model to a Artifacts folder
    """
    try:
        # Ensure the model directory exists
        os.makedirs(MODEL_DIR, exist_ok=True)
        
         # Set environment variable to auto-accept TOS if flag is passed
        if accept_tos:
            os.environ["COQUI_TOS_AGREED"] = "1"
            logger.info("Auto-accepting terms of service for non-interactive environments")
        
        # Create a custom ModelManager with your desired cache directory
        manager = ModelManager(
            models_file=TTS.get_models_file_path(),
            output_prefix=MODEL_DIR,
            progress_bar=True,
            verbose=True
        )
        
        # Download the model to your specified location
        model_path, config_path, model_item = manager.download_model("tts_models/multilingual/multi-dataset/xtts_v2")
        
        logger.info(f"Model downloaded to: {model_path}")
        logger.info(f"Config downloaded to: {config_path}")
                
    except Exception as e:
        logger.error(f"Failed to download the model: {str(e)}")
        raise CustomException(f"Model download failed: {str(e)}", sys)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download pretrained TTS model")
    parser.add_argument("-y", "--accept-tos", action="store_true", 
                      help="Automatically accept terms of service (for non-interactive environments)")
    args = parser.parse_args()
    
    download_pretrained_model(accept_tos=args.accept_tos)