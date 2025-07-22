import os
import sys
from config.paths_config import *
from pydub import AudioSegment
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

def process_audio(input_path,output_path):
    """
    Processes the uploaded audio file to save in the specific WAV format.
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input audio file not found at {input_path}")

        # Ensure the directory for output exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            # Load the audio file
            audio = AudioSegment.from_file(input_path)
            
            # Export the audio to the desired format
            audio.export(output_path, format="wav")
            logger.info(f"Audio processed and saved to {output_path}")
            
            # Clean up the original file after processing
            os.remove(input_path)
            logger.info(f"Original audio file {input_path} removed after processing.")
            
        except Exception as audio_error:
            # More specific handling for pydub errors
            logger.error(f"Error processing audio with pydub: {str(audio_error)}")
            if "ffmpeg" in str(audio_error).lower():
                raise CustomException(f"FFmpeg error - please ensure FFmpeg is installed properly. Error: {str(audio_error)}", sys)
            raise CustomException(f"Failed to process audio format: {str(audio_error)}", sys)
        
        

    except FileNotFoundError as fnf:
        logger.error(f"File not found: {str(fnf)}")
        raise CustomException(f"Audio processing failed: {str(fnf)}", sys)
    except Exception as e:
        logger.error(f"Failed to process audio: {str(e)}")
        raise CustomException(f"Audio processing failed: {str(e)}", sys)