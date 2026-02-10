"""
Logging utilities for AI Research Bot
"""
import logging
import os
from datetime import datetime
import config


def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Get log level
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("="*70)
    logger.info("Logging system initialized")
    logger.info(f"Log level: {config.LOG_LEVEL}")
    logger.info(f"Log file: {config.LOG_FILE}")
    logger.info("="*70)


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance for a module
    
    Args:
        name: Module name (use __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Custom log handler for Discord notifications (future use)
class DiscordLogHandler(logging.Handler):
    """Custom handler to send critical errors to Discord"""
    
    def __init__(self, discord_webhook_url=None):
        super().__init__()
        self.webhook_url = discord_webhook_url
        self.setLevel(logging.ERROR)
    
    def emit(self, record):
        """Send log record to Discord"""
        if not self.webhook_url:
            return
        
        try:
            import requests
            
            log_entry = self.format(record)
            payload = {
                'content': f"🚨 **Error Alert**\n```\n{log_entry}\n```"
            }
            
            requests.post(self.webhook_url, json=payload)
        except Exception:
            pass  # Don't let logging errors break the application
