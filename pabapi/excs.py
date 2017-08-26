# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class UnhandledError(Exception):
    def __init__(self, message, *args):
        super(UnhandledError, self).__init__(message, *args)


class ConfigFileNotFound(Exception):
    def __init__(self, message, *args):
        super(ConfigFileNotFound, self).__init__(message, *args)


class ConfigFileInvalid(Exception):
    def __init__(self, message, *args):
        super(ConfigFileInvalid, self).__init__(message, *args)


class MissingSchema(Exception):
    def __init__(self, message, *args):
        super(MissingSchema, self).__init__(message, *args)


class RecordExists(Exception):
    def __init__(self, message, *args):
        super(RecordExists, self).__init__(message, *args)


class RecordDoesNotExist(Exception):
    def __init__(self, message, *args):
        super(RecordDoesNotExist, self).__init__(message, *args)
