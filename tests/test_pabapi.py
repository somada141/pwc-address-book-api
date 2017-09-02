#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pabapi.py` module."""

from __future__ import unicode_literals

import falcon.testing
import ujson

from pabapi import pabapi

from . import utils


class TestPabApi(falcon.testing.TestCase):
    def setUp(self):
        super(TestPabApi, self).setUp()

        self.app = pabapi.build_app(
            path_config_file=utils.get_test_config_path()
        )

        self.tap = utils.setup_db()

    def tearDown(self):
        utils.teardown_db(tap=self.tap)

    def test_get_ping(self):
        response_refr = {"status": "OK"}

        response_eval = self.simulate_get(path="/ping").json

        self.assertEqual(response_refr, response_eval)

    def test_post_contacts_get(self):
        response_refr = [
            {
                "contact_id": 1,
                "email": "john@doe.com",
                "name": "John Doe",
            },
            {
                "contact_id": 2,
                "email": "jane@doe.com",
                "name": "Jane Doe"
            },
        ]

        response_eval = self.simulate_post(path="/contacts/get").json

        self.assertEqual(response_refr, response_eval)

    def test_post_contacts_add(self):
        request_params = {
            "contacts": [
                {
                    "name": "Jimmy Doe",
                    "email": "jimmy@doe.com"
                }
            ]
        }
        request_body = ujson.dumps(request_params)

        response_refr = {
            "contacts": {
                "accepted": [
                    {
                        "email": "jimmy@doe.com",
                        "name": "Jimmy Doe"
                    }
                ],
                "rejected": []
            },
            "records": [
                {
                    "contact_id": 3,
                    "email": "jimmy@doe.com",
                    "name": "Jimmy Doe"
                }
            ]
        }

        response_eval = self.simulate_post(
            path="/contacts/add",
            body=request_body
        ).json

        self.assertEqual(response_refr, response_eval)

    def test_post_contacts_add_duplicate(self):
        request_params = {
            "contacts": [
                {
                    "name": "John Doe",
                    "email": "john@doe.com"
                }
            ]
        }
        request_body = ujson.dumps(request_params)

        response_refr = {
            "contacts": {
                "accepted": [],
                "rejected": [
                    {
                        "email": "john@doe.com",
                        "name": "John Doe"
                    }
                ]
            },
            "records": []
        }

        response_eval = self.simulate_post(
            path="/contacts/add",
            body=request_body
        ).json

        self.assertEqual(response_refr, response_eval)

    def test_post_contacts_update(self):
        request_params = {
            "contacts": [
                {
                    "name": "Jane Deer",
                    "email": "jane@doe.com"
                }
            ]
        }
        request_body = ujson.dumps(request_params)

        response_refr = {
            "contacts": {
                "accepted": [
                    {
                        "email": "jane@doe.com",
                        "name": "Jane Deer"
                    }
                ],
                "rejected": []
            },
            "records": [
                {
                    "contact_id": 2,
                    "email": "jane@doe.com",
                    "name": "Jane Deer"
                }
            ]
        }

        response_eval = self.simulate_post(
            path="/contacts/update",
            body=request_body
        ).json

        self.assertEqual(response_refr, response_eval)

    def test_post_contacts_update_missing(self):
        request_params = {
            "contacts": [
                {
                    "name": "Jane Williams",
                    "email": "jane@williams.com"
                }
            ]
        }
        request_body = ujson.dumps(request_params)

        response_refr = {
            "contacts": {
                "rejected": [
                    {
                        "email": "jane@williams.com",
                        "name": "Jane Williams"
                    }
                ],
                "accepted": []
            },
            "records": []
        }

        response_eval = self.simulate_post(
            path="/contacts/update",
            body=request_body
        ).json

        self.assertEqual(response_refr, response_eval)

    def test_schema_invalid_request(self):
        request_params = {
            "contacts": 1
        }
        request_body = ujson.dumps(request_params)

        response_refr = {
            "title": "InvalidRequest",
            "description": ("Invalid parameters provided. Exception: Value 1 "
                            "for field '<obj>.contacts' is not of type array")
        }

        response_eval = self.simulate_post(
            path="/contacts/update",
            body=request_body
        ).json

        self.assertEqual(response_refr, response_eval)

    def test_upload_csv(self):
        path_csv_file = utils.get_test_csv_path()

        response_refr = [
            {
                'email': 'james@doe.com',
                'name': 'James Doe'
            },
            {
                'email': u'janice@doe.com',
                'name': u'Janice Doe'
            },
            {
                'email': u'jane@doe.com',
                'name': u'Jane Williams'
            }
        ]

        with open(path_csv_file, str("r")) as csv_file:
            response_eval = self.simulate_post(
                path="/upload",
                body=csv_file.read()
            ).json

        self.assertEqual(response_refr, response_eval)
