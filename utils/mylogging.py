import logging

# Define colors using ANSI escape codes
LOG_COLORS = {
    'DEBUG': '\033[94m',     # Blue
    'INFO': '\033[92m',      # Green
    'WARNING': '\033[93m',   # Yellow
    'ERROR': '\033[91m',     # Red
    'CRITICAL': '\033[1;91m',# Bold Red
    'RESET': '\033[0m'       # Reset color
}

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = LOG_COLORS.get(record.levelname, LOG_COLORS['RESET'])
        reset = LOG_COLORS['RESET']
        message = super().format(record)
        return f"{color}{message}{reset}"

# Set up the logger
formatter = ColoredFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)