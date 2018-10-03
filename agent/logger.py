import logging
import os


def create_logger(args):
    try:
        logger = setup_logger(args.verbose)
    except AttributeError:
        # Args.verbose is not defined (because the program was launched with the daemon stop command, etc...)
        logger = setup_logger(False)
    return logger


def setup_logger(verbose):
    logger = logging.getLogger("insideapp-agent")
    logger.setLevel(logging.DEBUG)

    # Setup file logging.
    log_filename = '/var/log/insideapp/insideapp-agent.log'
    if not os.path.exists(os.path.dirname(log_filename)):
        os.makedirs(os.path.dirname(log_filename))
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    fhFormatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')
    fh.setFormatter(fhFormatter)
    logger.addHandler(fh)

    # Setup console logging
    ch = logging.StreamHandler()
    if verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)
    chFormatter = logging.Formatter(
        '%(levelname)s - %(message)s')
    ch.setFormatter(chFormatter)
    logger.addHandler(ch)

    return logger
