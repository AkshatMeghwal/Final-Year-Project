import logging

# Configure logging
logging.basicConfig(
    filename='debug.log',  # Log file name
    level=logging.DEBUG,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

# Example log messages
# logging.debug('This is a debug message.')
# logging.info('This is an info message.')
# logging.warning('This is a warning message.')
# logging.error('This is an error message.')
# logging.critical('This is a critical message.')

# print("Logging completed. Check 'debug.log' for details.")
