# https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/

import sys
import logging

from loguru import logger


__all__ = ("setup_logging",)

LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} <lvl>| {level: ^6} |</> {message}"


class InterceptHandler(logging.Handler):  # pragma: no cover
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(debug=False):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.getLevelName("DEBUG" if debug else "INFO"))

    logging.getLogger("steam").setLevel(logging.ERROR)  # prevent log pollution

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        other_logger = logging.getLogger(name)
        other_logger.handlers = []
        other_logger.propagate = True

    # configure loguru
    logger.level("INFO", color="<m>")
    logger.configure(handlers=({"sink": sys.stdout, "colorize": True, "format": LOG_FORMAT},))
