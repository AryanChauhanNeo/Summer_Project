"""
utils/logging_config.py
========================
One place to configure logging for the whole backend, so every module
just does `logging.getLogger(__name__)` and gets consistent formatting.
"""

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging handlers and format. Safe to call once at startup."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
