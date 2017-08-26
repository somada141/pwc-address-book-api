# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import inspect

import ujson
import validictory
import decorator

from . import excs


def validate_parameters():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        # Get the arguments with which the method was called.
        func_args = inspect.getargspec(func).args

        # Get the class name by getting the type name of the first argument
        # which in the case of a method should be the class object itself.
        name_class = type(args[0]).__name__

        # Get the method name.
        name_method = func.func_name

        # Compile the schema name (following the convention).
        name_schema = "schema_{0}_{1}".format(name_class, name_method)

        # Retrieve the reference to this module.
        thismodule = sys.modules[__name__]

        # If the conventional schema name exists then use it to validate the
        # parameters. If not then the method was decorated without a schema
        # being defined and an exception is thrown.
        if hasattr(thismodule, name_schema):
            schema_json = getattr(thismodule, name_schema)
        else:
            msg_fmt = "JSON schema '{0}' not available".format(name_schema)
            raise excs.MissingSchema(msg_fmt)

        # Create a dictionary with the argument names and values for this
        # method call.
        parameters = {k: v for k, v in zip(func_args, args)}

        try:
            # If the schema was provided in the form of a string (str or
            # unicode) then decode it assuming its in a JSON format. Otherwise,
            # if the schema is in the form of a dict use as is.
            if isinstance(schema_json, str) or isinstance(schema_json, unicode):
                _schema = ujson.loads(schema_json)
            elif isinstance(schema_json, dict):
                _schema = schema_json
            else:
                raise NotImplementedError

            # Perfrom the validation.
            validictory.validate(
                data=parameters,
                schema=_schema,
                required_by_default=False,
                blank_by_default=True
            )

        # Re-raise any exceptions caused during the schema decoding or
        # validation.
        except Exception as exc:
            raise exc
        return func(*args, **kwargs)

    return wrapper
