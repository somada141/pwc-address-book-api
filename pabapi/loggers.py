# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import logging
import logging.handlers

import colorlog


def create_logger(
        logger_name,
        logger_level="DEBUG",
        project_name="pwc-address-book-api",
        do_log_stdout=True,
        do_log_syslog=True,
        do_color_logs=True,
):

    # Create the logger with the appropriate name.
    logger = logging.getLogger(name=logger_name)

    # Set logger's log-level.
    logger.setLevel(logger_level)

    # If the logger has already been configured (module reloads) then don't
    # configure it.
    if logger.handlers:
        return logger

    # Assemble the logging format.
    fmt_tmpl = ("{0}: %(process)d %(processName)s %(asctime)-15s "
                "%(levelname)-8s %(name)-10s %(funcName)s %(message)s")
    fmt = fmt_tmpl.format(project_name)

    # Create a colourful formatter (should one be needed).
    formatter_w_color = colorlog.ColoredFormatter(
        fmt="%(log_color)s" + fmt,
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        reset=True,
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    formatter_wo_color = logging.Formatter(fmt=fmt)

    # Create an 'stdout' logging handler, set its output format, and add to the
    # logger (if enabled).
    if do_log_stdout:
        handler_stdout = logging.StreamHandler(sys.stdout)
        handler_stdout.setFormatter(
            formatter_w_color if do_color_logs else formatter_wo_color
        )
        logger.addHandler(handler_stdout)

    # Create a 'syslog' logging handler, set its output format, and add to the
    # logger (if enabled).
    if do_log_syslog and ("darwin" not in sys.platform):
        handler_syslog = logging.handlers.SysLogHandler(address="/dev/log")
        handler_syslog.setFormatter(formatter_wo_color)
        logger.addHandler(handler_syslog)

    return logger
