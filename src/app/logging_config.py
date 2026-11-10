
import logging
from pathlib import Path
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler


# Store request ID
request_id_var = ContextVar("request_id", default="SYSTEM")


# Add request ID to each log record
class RequestIDFilter(logging.Filter):

    def filter(self, record):
        record.request_id = request_id_var.get()
        return True


def setup_logging():

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(request_id)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    console.addFilter(RequestIDFilter())

    # Application log handler
    app_file = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    app_file.setLevel(logging.DEBUG)
    app_file.setFormatter(formatter)
    app_file.addFilter(RequestIDFilter())

    # Error log handler
    error_file = RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    error_file.setLevel(logging.ERROR)
    error_file.setFormatter(formatter)
    error_file.addFilter(RequestIDFilter())

    # Configure root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()

    root.addHandler(console)
    root.addHandler(app_file)
    root.addHandler(error_file)


def get_logger(name):
    return logging.getLogger(name)
