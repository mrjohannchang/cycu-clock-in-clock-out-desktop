import importlib.metadata
import logging


formatter: logging.Formatter = logging.Formatter(
    '%(levelname)s: %(asctime)s'
    f' v{importlib.metadata.version("cycu-clock-in-clock-out-app")}'
    ' %(filename)s:%(lineno)d %(message)s')

logger: logging.Logger = logging.getLogger('CYCU-Clock-in-Clock-out')
logger.setLevel(logging.DEBUG)

file_handler: logging.FileHandler = logging.FileHandler('cycu-clco.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def get_logger() -> logging.Logger:
    return logger
