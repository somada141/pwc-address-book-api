#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pabapi.py` module."""

from __future__ import unicode_literals

from falcon import testing

import pabapi

from . import utils


class TestConfig(testing.TestCase):

    def test_import_config(self):
        cfg = pabapi.config.import_config(
            fname_config_file=utils.get_test_config_path()
        )

        self.assertEqual(cfg.logger_level, "CRITICAL")
        self.assertEqual(cfg.sql_username, "test")
        self.assertEqual(cfg.sql_password, "2wk0mC49a7RWuxvSN2aw3REo83IHgz")
        self.assertEqual(cfg.sql_host, "localhost")
        self.assertEqual(cfg.sql_port, 3306)
        self.assertEqual(cfg.sql_db, "test")

    def test_import_config_missing(self):

        self.assertRaises(
            pabapi.excs.ConfigFileNotFound,
            pabapi.config.import_config,
            fname_config_file="/this/does/not/exist.json"
        )

    def test_validate_config_invalid(self):
        cfg = pabapi.config.import_config(
            fname_config_file=utils.get_test_config_path()
        )

        cfg["sql_port"] = "3306"

        self.assertRaises(
            pabapi.excs.ConfigFileInvalid,
            pabapi.config.validate_config,
            config_instance=cfg
        )
