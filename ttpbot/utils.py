import logging

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOG_LEVEL = logging.DEBUG


def configure_logger(cls, log_level=None, stream_handling=True):
    """ Takes a python class and returns a logger for that class. Convenience
    method.

    """
    logger_name = cls.__name__ if cls else 'default'
    logger = logging.getLogger(logger_name) if cls else logging.getLogger()
    log_level = DEFAULT_LOG_LEVEL if not log_level else log_level
    logger.setLevel(log_level)

    formatter = logging.Formatter(LOGGING_FORMAT)

    if stream_handling:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def load_file(file_name, file_lines=None, logger=None):
    """ Utility method for loading any configuration files. """
    try:
        with open(file_name,'r') as file_contents:
            file_lines = file_contents.readlines()
    except IOError:
        if logger:
            logger.error(
                "The file %s was not found. Help may not work.".format(
                file_name))
    return file_lines