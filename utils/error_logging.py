import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)


def log_error(error, **kwargs):
    try:
        msg = str(error)
        if hasattr(error, "message"):
            msg = str(error.message)

        for arg in kwargs:
            msg += f" | {arg}: {kwargs[arg]}"
        logging.error(msg)
    except Exception as e:
        logging.error(e)
        