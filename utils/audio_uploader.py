import os
import sys
from utils.custom_exception import CustomException
from utils.logger import get_logger
from config.paths_config import *
import time

logger = get_logger(__name__)

def upload_audio(file):
    if not file:
        logger.error("No file provided for upload.")
        raise CustomException("No file provided for upload.")
    
    extension = os.path.splitext(file.filename)[1]

    new_filename = f"uploaded_voice{extension}"
    uploaded_path = os.path.join(UPLOAD_DIR, new_filename)
    
    # Ensure the upload directory exists
    os.makedirs(os.path.dirname(uploaded_path), exist_ok=True)
    
    # Save the file to disk
    file.save(uploaded_path)
    
    # Verify the file exists and is accessible before proceeding
    if not os.path.exists(uploaded_path):
        logger.error(f"File was not properly saved to {uploaded_path}")
        raise CustomException(f"Failed to save uploaded file to {uploaded_path}")
    
    # Adding a small delay to ensure file is completely written and released
    
    time.sleep(.1)  # 500ms delay to ensure file I/O completes
    
    logger.info(f"Uploading audio file to {uploaded_path}")
    return uploaded_path
    
