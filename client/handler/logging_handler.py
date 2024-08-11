import logging

# logging handler
logging.basicConfig(
    filename='error.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

def log_error(message: str):
    logging.error(message)
