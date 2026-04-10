"""File validation utilities for resume uploads."""
import os
from werkzeug.utils import secure_filename

ALLOWED_FORMATS = {'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
MIN_FILE_SIZE = 10 * 1024  # 10KB in bytes

def validate_file_format(filename: str) -> tuple[bool, str]:
    """
    Validate that the file is a PDF.
    
    Args:
        filename: The uploaded filename
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not filename or filename == '':
        return False, "No file selected."
    
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if file_ext not in ALLOWED_FORMATS:
        return False, f"Invalid file format. Only PDF files are allowed. (Got: .{file_ext})"
    
    return True, "File format valid."


def validate_file_size(file_path: str) -> tuple[bool, str]:
    """
    Validate file size is within acceptable range.
    
    Args:
        file_path: Path to the uploaded file
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        file_size = os.path.getsize(file_path)
        
        if file_size < MIN_FILE_SIZE:
            size_kb = file_size / 1024
            return False, f"File is too small ({size_kb:.1f} KB). Minimum size is 10 KB."
        
        if file_size > MAX_FILE_SIZE:
            size_mb = file_size / (1024 * 1024)
            return False, f"File is too large ({size_mb:.1f} MB). Maximum size is 5 MB."
        
        size_kb = file_size / 1024
        return True, f"File size valid ({size_kb:.1f} KB)."
    
    except Exception as e:
        return False, f"Error checking file size: {str(e)}"


def validate_upload(filename: str, file_path: str) -> tuple[bool, str]:
    """
    Complete file validation (format + size).
    
    Args:
        filename: The uploaded filename
        file_path: Path to the uploaded file
        
    Returns:
        Tuple of (is_valid, message)
    """
    
    format_valid, format_msg = validate_file_format(filename)
    if not format_valid:
        return False, format_msg
    
    
    size_valid, size_msg = validate_file_size(file_path)
    if not size_valid:
        return False, size_msg
    
    return True, "File validation passed."
