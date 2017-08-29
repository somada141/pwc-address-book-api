# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import ujson
import validictory
import attrdict

from . import excs

config_schema_default = {
    "type": "object",
    "required": [
        # General Settings.
        "logger_level",
        # SQL Server Configuration Settings.
        "sql_host", "sql_port", "sql_username", "sql_password", "sql_db"
    ],
    "properties": {
        "logger_level": {
            "type": "string",
            "description": ("The minimum level of `logging` messages that will "
                            "be emitted"),
            "enum": [
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL"
            ]
        },
        # SQL Server Configuration Settings.
        "sql_host": {
            "type": "string", "description": "MySQL server host."
        },
        "sql_port": {
            "type": "integer", "description": "MySQL server port."
        },
        "sql_username": {
            "type": "string", "description": "MySQL server username."
        },
        "sql_password": {
            "type": "string", "description": "MySQL server password."
        },
        "sql_db": {
            "type": "string", "description": "MySQL server database name."
        },
    }
}


def load_config_file(fname_config_file):
    if (
            not os.path.exists(fname_config_file) or
            not os.path.isfile(fname_config_file)
    ):
        msg = "Config file '{0}' not found or not a file."
        msg_fmt = msg.format(fname_config_file)
        raise excs.ConfigFileNotFound(msg_fmt)

    with open(fname_config_file, str("r")) as finp:
        config = ujson.load(finp)

    return config


def validate_config(config_instance, config_schema=None):
    if config_schema is None:
        config_schema = config_schema_default

    try:
        validictory.validate(
            data=config_instance,
            schema=config_schema,
            required_by_default=False,
            blank_by_default=True
        )
    except Exception as exc:
        raise excs.ConfigFileInvalid(exc.message)

    return True


def import_config(fname_config_file):
    config = load_config_file(fname_config_file=fname_config_file)

    validate_config(config_instance=config, config_schema=config_schema_default)

    return attrdict.AttrDict(config)
