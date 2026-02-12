import logging

from rich.logging import RichHandler


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()],
    )

    return logging.getLogger("email_composer")
