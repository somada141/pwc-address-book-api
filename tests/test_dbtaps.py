#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dbtaps.py` module."""

from __future__ import unicode_literals

import unittest

import pabapi

from . import utils


class TestTapPab(unittest.TestCase):
    """Tests for `pabapi.dbtaps.TapPab` class."""

    def setUp(self):

        self.tap = utils.setup_db()

    def tearDown(self):
        """Tears down fixtures"""

        utils.teardown_db(tap=self.tap)

    def test_get_contact_by_email(self):
        contact_obj = self.tap.get_contact_by_email(
            contact_email="john@doe.com"
        )

        self.assertEqual(contact_obj.contact_id, 1)
        self.assertEqual(contact_obj.name, "John Doe")
        self.assertEqual(contact_obj.email, "john@doe.com")

    def test_get_contacts(self):

        contact_objs = self.tap.get_contacts()

        self.assertEqual(len(contact_objs), 2)

    def test_has_contact_true(self):

        self.assertTrue(
            self.tap.has_contact_by_email(contact_email="john@doe.com")
        )

    def test_has_contact_false(self):
        self.assertFalse(
            self.tap.has_contact_by_email(contact_email="johnny@doe.com")
        )

    def test_add_contact(self):

        contact_obj = self.tap.add_contact(
            contact_name="Jimmy Doe",
            contact_email="jimmy@doe.com"
        )

        self.assertEqual(contact_obj.contact_id, 3)
        self.assertEqual(contact_obj.name, "Jimmy Doe")
        self.assertEqual(contact_obj.email, "jimmy@doe.com")

    def test_update_contact_name(self):

        contact_obj = self.tap.update_contact_name(
            contact_name="Jane Deer",
            contact_email="jane@doe.com"
        )

        self.assertEqual(contact_obj.contact_id, 2)
        self.assertEqual(contact_obj.name, "Jane Deer")
        self.assertEqual(contact_obj.email, "jane@doe.com")

    def test_add_duplicate_contact(self):

        self.assertRaises(
            pabapi.excs.RecordExists,
            self.tap.add_contact,
            contact_name="John Doe",
            contact_email="john@doe.com"
        )

    def test_update_missing_contact(self):

        self.assertRaises(
            pabapi.excs.RecordDoesNotExist,
            self.tap.update_contact_name,
            contact_name="Johnny Doe",
            contact_email="johnny@doe.com"
        )

    def test_orm_to_dict(self):

        contact_obj = self.tap.get_contact_by_email(
            contact_email="john@doe.com"
        )

        contact_dict_refr = {
            "contact_id": 1,
            "name": "John Doe",
            "email": "john@doe.com",
        }

        contact_dict_eval = contact_obj.to_dict(serialisable=True)

        self.assertEqual(contact_dict_refr, contact_dict_eval)

    def test_orm_to_string(self):

        contact_obj = self.tap.get_contact_by_email(
            contact_email="john@doe.com"
        )

        contact_string_eval = contact_obj.to_string()

        self.assertIn("contact_id='1'", contact_string_eval)
        self.assertIn("name='John Doe'", contact_string_eval)
        self.assertIn("email='john@doe.com'", contact_string_eval)
