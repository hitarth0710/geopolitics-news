"""Logging configuration for production-ready application."""
import logging
import sys
from datetime import datetime
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for development."""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON formatter for production logging."""
    
    def format(self, record):
        import json
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, 'extra'):
            log_record.update(record.extra)
        
        return json.dumps(log_record)


def setup_logging(
    level: str = "INFO",
    json_logs: bool = False,
    log_file: Optional[str] = None
) -> logging.Logger:
    """Configure application logging.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Use JSON format for production
        log_file: Optional file path for log output
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("geopolitics")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    if json_logs:
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
    
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    
    return logger


# Global logger instance
logger = setup_logging()
