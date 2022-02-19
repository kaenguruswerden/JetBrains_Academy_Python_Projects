import logging
import shutil


def log_and_print(msg: str) -> None:
    """Print passed message to the console and the log file."""
    print(msg)
    logger.debug(msg)


def get_input_and_log(msg: str) -> str:
    """Return a user input. Print passed message to the console and the log file.
    The user input only gets written to the log."""
    log_and_print(msg)
    user_input = input("> ")
    logger.debug("> " + user_input)
    return user_input


def save_log_to_file(file_name: str) -> None:
    """Copy the content of the log file to file with passed file name."""
    shutil.copyfile(DEBUG_FILE_NAME, file_name)


DEBUG_FILE_NAME = "debug_log_file.txt"

logging.basicConfig(format="%(message)s",
                    level="DEBUG",
                    handlers=[logging.FileHandler(DEBUG_FILE_NAME, mode="w", encoding="UTF-8")]
                    )
logger = logging.getLogger()
