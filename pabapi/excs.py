# -*- coding: utf-8 -*-

""" Custom application-wide exception classes.

This module contains custom exception classes that can be used to wrap other
exception and allow for consistent error-handling across the application.
"""

from __future__ import unicode_literals


class UnhandledError(Exception):
    def __init__(self, message, *args):
        super(UnhandledError, self).__init__(message, *args)


class ConfigFileNotFound(Exception):
    """Exception thrown when a JSON configuration file is missing."""
    def __init__(self, message, *args):
        super(ConfigFileNotFound, self).__init__(message, *args)


class ConfigFileInvalid(Exception):
    """Exception thrown when a JSON configuration file is invalid."""
    def __init__(self, message, *args):
        super(ConfigFileInvalid, self).__init__(message, *args)


class MissingSchema(Exception):
    """Exception thrown when the schema is missing

    This exception is meant to be thrown by the `validate_parameters` decorator
    under the `schemata.py` module
    """
    def __init__(self, message, *args):
        super(MissingSchema, self).__init__(message, *args)


class RecordExists(Exception):
    """Exception thrown when a required DB record does not exist."""
    def __init__(self, message, *args):
        super(RecordExists, self).__init__(message, *args)


class RecordDoesNotExist(Exception):
    """Exception thrown when an existing DB record is overwritten."""
    def __init__(self, message, *args):
        super(RecordDoesNotExist, self).__init__(message, *args)
