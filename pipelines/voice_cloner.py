import os
import sys
import torch
import gc
        
from src.model_loader import load_model
from src.audio_processor import process_audio

from config.paths_config import PROCESSED_VOICE_PATH, GENERATED_VOICE_PATH, LANGUAGE
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

def voice_cloning_pipeline(script, 
                          uploaded_voice_path, 
                          processed_voice_path=PROCESSED_VOICE_PATH, 
                          generated_voice_path=GENERATED_VOICE_PATH,
                          language=LANGUAGE,
                          cached_model=None):
    """
    Main pipeline for voice cloning with model caching support.
    
    Args:
        script (str): Text to be spoken in cloned voice
        uploaded_voice_path (str): Path to uploaded voice sample
        processed_voice_path (str): Path for processed voice file
        generated_voice_path (str): Path for output generated voice
        language (str): Language code for TTS (default from config)
        cached_model: Pre-loaded TTS model (optional)
    
    Returns:
        str: Path to generated voice file
    """
    try:
        logger.info(f"Starting voice cloning pipeline for script: {script[:50]}...")
        
        # Step 1: Process the uploaded audio file
        process_audio(uploaded_voice_path, processed_voice_path)
        logger.info("Audio processing completed")

        # Step 2: Load or use cached TTS model
        tts = cached_model if cached_model else load_model()
        logger.info("TTS model ready")

        # Step 3: Generate speech using the processed voice
        tts.tts_to_file(
            text=script, 
            file_path=generated_voice_path,
            speaker_wav=processed_voice_path,
            language=language
        )

        logger.info(f"Voice cloning completed. Generated voice saved to {generated_voice_path}")
        
        # Clear Python garbage collection
        gc.collect()
        
        # Clear CUDA cache if available
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.reset_accumulated_memory_stats()
        
        # Force garbage collection again
        gc.collect()

        return generated_voice_path

    except Exception as e:
        logger.error(f"Voice cloning pipeline failed: {str(e)}")
        raise CustomException(f"Voice cloning failed: {str(e)}", sys)

if __name__ == "__main__":
    ## Example usage of the voice cloning pipeline
    try:
        script = "Hello, this is a test of the voice cloning pipeline."
        language = "en"  # Example language code
        generated_voice = voice_cloning_pipeline(
            script=script,
            uploaded_voice_path="path/to/uploaded_voice.wav",
            language=language
        )
        logger.info(f"Generated voice file: {generated_voice}")
    except CustomException as e:
        logger.error(f"Pipeline error: {str(e)}")