"""
Helper utilities for AI Research Bot
"""
import os
from datetime import datetime
from typing import Optional


def create_directories():
    """Create necessary directories for the application"""
    directories = [
        'logs',
        'data',
        'output',
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")


def format_date(date_obj: Optional[datetime] = None, format_str: str = '%Y-%m-%d') -> str:
    """
    Format datetime object to string
    
    Args:
        date_obj: Datetime object (default: now)
        format_str: Format string
        
    Returns:
        Formatted date string
    """
    if date_obj is None:
        date_obj = datetime.now()
    
    return date_obj.strftime(format_str)


def truncate_text(text: str, max_length: int = 200, suffix: str = '...') -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_filename(filename: str) -> str:
    """
    Clean filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    if not os.path.exists(file_path):
        return 0.0
    
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def ensure_dir_exists(file_path: str):
    """
    Ensure directory exists for a file path
    
    Args:
        file_path: Path to file
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
