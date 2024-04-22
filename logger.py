import logging

# from sys import stdout
from config import config
import structlog

processors = [
    structlog.stdlib.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.format_exc_info,
    structlog.processors.JSONRenderer(),
]


base_logger = logging.getLogger("transcoder")
base_logger.setLevel(level=config["DEBUG_LEVEL"])

logger = structlog.wrap_logger(
    base_logger,
    processors=processors,
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    cache_logger_on_first_use=True,
)
