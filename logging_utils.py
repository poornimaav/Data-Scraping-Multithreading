import logging

class InfoAndErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {logging.INFO, logging.ERROR}

def setup_logging(log_filename):
    log_format = '%(asctime)s - %(levelname)s: %(message)s'
    
    # Configure logger to save INFO and ERROR logs to the specified log file
    logging.basicConfig(filename=log_filename, level=logging.INFO, format=log_format)
    logger = logging.getLogger()
    
    # Clear any existing handlers to avoid duplication
    logger.handlers.clear()

    # Add a handler for file logging with INFO level (captures INFO and ERROR levels)
    file_handler = logging.FileHandler(log_filename, mode='a')  # Append mode
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    # Add a handler for console output with INFO and ERROR levels
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.addFilter(InfoAndErrorFilter())  # Apply the filter to the console handler
    logger.addHandler(console_handler)

    return logger
