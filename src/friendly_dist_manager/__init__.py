"""User friendly Python distribution package manager"""
from os import environ
import logging
from pathlib import Path
from friendly_dist_manager.version import __version__


def _config_logger():
    """Configures the default logger for the package

    Currently only supports defining a custom logger for
    use by the unit test framework associated with the project
    """
    if "TFC_LOG_FILE" not in environ:
        return
    tfc_log_file = Path(environ["TFC_LOG_FILE"])
    log_file = tfc_log_file.parent / f"{tfc_log_file.stem}_subproc.log"
    global_log = logging.getLogger()
    global_log.setLevel(logging.DEBUG)

    verbose_format = "%(asctime)s(%(levelname)s->%(name)s:%(funcName)s):%(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    fmt = logging.Formatter(verbose_format, date_format)

    file_handler = logging.FileHandler(log_file, mode="w")
    level = environ.get("TFC_LOG_LEVEL", logging.getLevelName(logging.DEBUG))
    file_handler.setLevel(level)
    file_handler.setFormatter(fmt)
    global_log.addHandler(file_handler)


_config_logger()
