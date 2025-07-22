import os
import glob
from utils.logger import get_logger
from config.paths_config import UPLOAD_DIR, PROCESSED_DIR, GENERATED_DIR

logger = get_logger(__name__)

def cleanup_directory(directory_path, keep_current=False):
    """
    Clean up all files in a directory.
    
    Args:
        directory_path (str): Path to the directory to clean
        keep_current (bool): If True, keep files with 'current' in the name
    """
    try:
        if not os.path.exists(directory_path):
            return 0
        
        cleaned_files = 0
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if os.path.isfile(file_path):
                # Skip current files if keep_current is True
                if keep_current and 'current' in filename:
                    continue
                    
                try:
                    os.remove(file_path)
                    cleaned_files += 1
                    logger.info(f"Removed file: {file_path}")
                except OSError as e:
                    logger.warning(f"Failed to remove file {file_path}: {str(e)}")
        
        return cleaned_files
        
    except Exception as e:
        logger.error(f"Error cleaning directory {directory_path}: {str(e)}")
        return 0

def cleanup_all_files():
    """Clean up all old files in upload, processed, and generated directories."""
    total_cleaned = 0
    
    # Clean uploaded files (except current)
    total_cleaned += cleanup_directory(UPLOAD_DIR, keep_current=True)
    
    # Clean all processed files (they're temporary)
    total_cleaned += cleanup_directory(PROCESSED_DIR, keep_current=False)
    
    # Clean generated files (except current)
    total_cleaned += cleanup_directory(GENERATED_DIR, keep_current=True)
    
    logger.info(f"Total files cleaned: {total_cleaned}")
    return total_cleaned

def cleanup_old_files():
    """Clean up old files when a new upload starts."""
    total_cleaned = 0
    
    # Remove any existing uploaded files
    total_cleaned += cleanup_directory(UPLOAD_DIR, keep_current=False)
    
    # Remove any existing processed files
    total_cleaned += cleanup_directory(PROCESSED_DIR, keep_current=False)
    
    # Remove any existing generated files
    total_cleaned += cleanup_directory(GENERATED_DIR, keep_current=False)
    
    logger.info(f"Cleaned {total_cleaned} old files before new upload")
    return total_cleaned

def ensure_directories_exist():
    """Ensure all required directories exist."""
    directories = [UPLOAD_DIR, PROCESSED_DIR, GENERATED_DIR]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")
