# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import pabapi


def get_test_config_path():
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    dir_path_assets = os.path.join(dir_path, "assets")

    path_config_file = os.path.join(
        dir_path_assets,
        "pwc-address-book-api.json"
    )

    return path_config_file


def setup_db():
    cfg = pabapi.config.import_config(
        fname_config_file=get_test_config_path()
    )

    tap = pabapi.dbtaps.TapPab(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host=cfg.sql_host,
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db
    )

    # Add some contact fixtures to the `contacts` table.
    tap.add_contact(
        contact_name="John Doe",
        contact_email="john@doe.com"
    )
    tap.add_contact(
        contact_name="Jane Doe",
        contact_email="jane@doe.com"
    )

    return tap


def teardown_db(tap):
    # Truncate the `contacts` table.
    with tap.session_scope(refresh_objects=True) as session:
        session.execute("TRUNCATE TABLE contacts;")
