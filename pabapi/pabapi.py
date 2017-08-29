#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import falcon

from . import config
from . import loggers
from . import dbtaps
from . import resources


def build_app(path_config_file, *args, **kwargs):
    cfg = config.import_config(path_config_file)

    # create logger
    logger = loggers.create_logger(
        logger_name=__name__,
        logger_level=cfg.logger_level
    )

    # Create a tap into the MySQL database which will be passed to the API
    # resources.
    dbtap = dbtaps.TapPab(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host=cfg.sql_host,
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db
    )

    # falcon.API instances are callable WSGI apps
    app = falcon.API()

    msg_fmt = u"Initializing API resources"
    logger.info(msg_fmt)

    route_resources = {
        '/ping': resources.ResourcePing(
            dbtap=dbtap,
            logger_level=cfg.logger_level,
        ),
        '/contacts/get': resources.ResourceContactsGet(
            dbtap=dbtap,
            logger_level=cfg.logger_level,
        ),
        '/contacts/add': resources.ResourceContactsAdd(
            dbtap=dbtap,
            logger_level=cfg.logger_level,
        ),
        '/contacts/update': resources.ResourceContactsUpdate(
            dbtap=dbtap,
            logger_level=cfg.logger_level,
        ),
    }

    msg_fmt = u"Generating API routes"
    logger.info(msg_fmt)

    for route, resource in route_resources.items():
        app.add_route(str(route), resource)

    logger.info("API initialization complete")

    return app
