import os
import sys
import torch
from config.paths_config import MODEL_PATH, MODEL_CONFIG_PATH
from utils.logger import get_logger
from utils.custom_exception import CustomException

from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig, XttsArgs
from TTS.tts.configs.shared_configs import BaseDatasetConfig

logger = get_logger(__name__)
# Allowlist of safe globals
torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, XttsArgs, BaseDatasetConfig])

def load_model():
    try:
        if torch.cuda.is_available():
            device = "cuda"
            logger.info("CUDA is available. Using NVIDIA GPU for TTS.")
        else:
            device = "cpu"
            logger.info("No GPU available. Using CPU for TTS.")

    except Exception as e:
        device = "cpu"
        logger.warning("Failed to determine device. Defaulting to CPU.")
        raise CustomException(f"Device detection failed: {str(e)}",sys)
    
    try:
        
        # Check if the model file exists
        if not os.path.exists(os.path.join(MODEL_PATH,"model.pth")):
            logger.warning(f"Model file not found at {MODEL_PATH}. Attempting to download the model.")
            from src.download_pretrained_model import download_pretrained_model
            download_pretrained_model()
            logger.info(f"Model downloaded successfully to {MODEL_PATH}.")

        # Check if the config file exists
        if not os.path.exists(MODEL_CONFIG_PATH):
            raise FileNotFoundError(f"Config file not found at {MODEL_CONFIG_PATH}")
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise CustomException(f"Model or config file missing: {str(e)}", sys)
    
    try:
        logger.info(f"Loading TTS model from {MODEL_PATH} with config {MODEL_CONFIG_PATH}")
        tts = TTS(model_path=MODEL_PATH,config_path=MODEL_CONFIG_PATH).to(device)
    
    except Exception as e:
        logger.error(f"Failed to load TTS model: {str(e)}")
        raise CustomException(f"Model loading failed: {str(e)}", sys)

    return tts

if __name__ == "__main__":
    tts = load_model()
    logger.info("TTS model loaded successfully.")