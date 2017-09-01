# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import abc
import io

import falcon
import ujson
import validictory
import unicodecsv

from . import loggers
from . import excs


class ResourceBase(object):
    def __init__(self, dbtap, **kwargs):

        # Create class-level logger.
        self.logger = loggers.create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get(str("logger_level"), str("DEBUG"))
        )

        # Internalize arguments.
        self.dbtap = dbtap

    @abc.abstractproperty
    def schema(self):
        raise NotImplementedError

    def validate_parameters(self, parameters):

        # Perfrom the validation.
        try:
            validictory.validate(
                data=parameters,
                schema=self.schema,
                required_by_default=True,
                blank_by_default=False
            )
        except Exception as exc:
            msg_fmt = "Invalid parameters provided."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="InvalidRequest",
                description=msg_fmt + " Exception: {0}".format(exc.message)
            )

        return parameters

    def get_parameters(self, request):

        try:
            request_json = request.stream.read()
        except Exception as exc:
            msg_fmt = "Could not retrieve JSON body."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="InvalidRequest",
                description=msg_fmt + " Exception: {0}.".format(exc.message)
            )

        try:
            if (
                    isinstance(request_json, str) or
                    isinstance(request_json, unicode)
            ):
                parameters = ujson.loads(request_json)
            else:
                parameters = {}
        except Exception as exc:
            msg_fmt = "Could not decode JSON body."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="InvalidRequest",
                description=msg_fmt + " Exception: {0}.".format(exc.message)
            )

        if self.schema:
            self.validate_parameters(parameters=parameters)

        return parameters

    def prepare_response(self, response, results):

        try:
            response_json = ujson.dumps(results)
        except Exception as exc:
            msg = "Could not encode results '{0}' into JSON."
            msg_fmt = msg.format(results)
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_500,
                title="UnhandledError",
                description=msg_fmt + " Exception: {0}.".format(exc.message)
            )

        response.content_type = "application/json"
        response.body = response_json

        return response

    @abc.abstractmethod
    def execute(self, request, response):
        raise NotImplementedError


class ResourcePing(ResourceBase):
    def __init__(self, dbtap, **kwargs):
        super(ResourcePing, self).__init__(dbtap=dbtap, **kwargs)

    @property
    def schema(self):
        return {}

    def execute(self, request, response):
        msg_fmt = "Processing 'ping' request."
        self.logger.info(msg_fmt)

        results = {"status": "OK"}
        response = self.prepare_response(response=response, results=results)

        return response

    def on_get(self, request, response):
        return self.execute(request=request, response=response)


class ResourceContactsGet(ResourceBase):
    def __init__(self, dbtap, **kwargs):
        super(ResourceContactsGet, self).__init__(dbtap=dbtap, **kwargs)

    @property
    def schema(self):
        return {}

    def execute(self, request, response):
        msg_fmt = "Processing 'get_all_contacts' request."
        self.logger.info(msg_fmt)

        contact_objs = self.dbtap.get_contacts()

        contacts = [
            contact_obj.to_dict(serialisable=True)
            for contact_obj in contact_objs
        ]

        msg_fmt = "Returning {0} contacts.".format(len(contacts))
        self.logger.info(msg_fmt)

        response = self.prepare_response(response=response, results=contacts)

        return response

    def on_post(self, request, response):
        return self.execute(request=request, response=response)


class ResourceContactManipulationBase(ResourceBase):
    _schema = {
        "type": "object",
        "required": [
            "contacts"
        ],
        "properties": {
            "contacts": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {
                    "type": "object",
                    "required": [
                        "name",
                        "email"
                    ],
                    "properties": {
                        "name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 180
                        },
                        "email": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 180
                        }
                    }
                }
            }
        }
    }

    def __init__(self, dbtap, **kwargs):
        super(ResourceContactManipulationBase, self).__init__(
            dbtap=dbtap,
            **kwargs
        )

    @property
    def schema(self):
        return self._schema

    def add_contact(self, contact_name, contact_email):

        try:
            contact_obj = self.dbtap.add_contact(
                contact_name=contact_name,
                contact_email=contact_email
            )
        except excs.RecordExists:
            msg = "Contact with email '{0}' already exists."
            msg_fmt = msg.format(contact_email)
            self.logger.warning(msg_fmt)
            return None

        msg_fmt = "New contact '{0}' added".format(contact_obj)
        self.logger.info(msg_fmt)

        contact_dict = contact_obj.to_dict(serialisable=True)

        return contact_dict

    def update_contact(self, contact_name, contact_email):

        try:
            contact_obj = self.dbtap.update_contact_name(
                contact_name=contact_name,
                contact_email=contact_email
            )
        except excs.RecordDoesNotExist:
            msg = "Contact with email '{0}' does not exist."
            msg_fmt = msg.format(contact_email)
            self.logger.warning(msg_fmt)
            return None

        msg_fmt = "Contact '{0}' updated".format(contact_obj)
        self.logger.info(msg_fmt)

        contact_dict = contact_obj.to_dict(serialisable=True)

        return contact_dict

    @abc.abstractmethod
    def execute(self, request, response):
        raise NotImplementedError


class ResourceContactsAdd(ResourceContactManipulationBase):

    def __init__(self, dbtap, **kwargs):
        super(ResourceContactsAdd, self).__init__(dbtap=dbtap, **kwargs)

    def execute(self, request, response):
        msg_fmt = "Processing 'add_contacts' request."
        self.logger.info(msg_fmt)

        # Retrieve and validate the incoming parameters against the class
        # JSON schema.
        parameters = self.get_parameters(request=request)

        # Retrieve the incoming contacts.
        contacts = parameters["contacts"]

        msg_fmt = "Processing {0} contact(s)".format(len(contacts))
        self.logger.debug(msg_fmt)

        # Create an empty `results` dictionary that will hold the accepted
        # and/or rejected contacts (accounting for possible duplicates).
        results = {
            "contacts": {
                "accepted": [],
                "rejected": [],
            },
            "records": []
        }

        for contact in contacts:
            contact_dict = self.add_contact(
                contact_name=contact["name"],
                contact_email=contact["email"],
            )

            if contact_dict:
                results["contacts"]["accepted"].append(contact)
                results["records"].append(contact_dict)
            else:
                results["contacts"]["rejected"].append(contact)

        msg = "Accepted {0} out of {1} contacts"
        msg_fmt = msg.format(
            len(results["contacts"]["accepted"]),
            len(contacts)
        )
        self.logger.info(msg_fmt)

        response = self.prepare_response(response=response, results=results)

        return response

    def on_post(self, request, response):
        return self.execute(request=request, response=response)


class ResourceContactsUpdate(ResourceContactManipulationBase):

    def __init__(self, dbtap, **kwargs):
        super(ResourceContactsUpdate, self).__init__(dbtap=dbtap, **kwargs)

    def execute(self, request, response):
        msg_fmt = "Processing 'update_contacts' request."
        self.logger.info(msg_fmt)

        # Retrieve and validate the incoming parameters against the class
        # JSON schema.
        parameters = self.get_parameters(request=request)

        # Retrieve the incoming contacts.
        contacts = parameters["contacts"]

        msg_fmt = "Processing {0} contact(s)".format(len(contacts))
        self.logger.debug(msg_fmt)

        # Create an empty `results` dictionary that will hold the accepted
        # and/or rejected contacts (accounting for possible duplicates).
        results = {
            "contacts": {
                "accepted": [],
                "rejected": [],
            },
            "records": []
        }

        for contact in contacts:
            contact_dict = self.update_contact(
                contact_name=contact["name"],
                contact_email=contact["email"],
            )

            if contact_dict:
                results["contacts"]["accepted"].append(contact)
                results["records"].append(contact_dict)
            else:
                results["contacts"]["rejected"].append(contact)

        msg = "Accepted {0} out of {1} contacts"
        msg_fmt = msg.format(
            len(results["contacts"]["accepted"]),
            len(contacts)
        )
        self.logger.info(msg_fmt)

        response = self.prepare_response(response=response, results=results)

        return response

    def on_post(self, request, response):
        return self.execute(request=request, response=response)


class ResourceUploadCsv(object):
    def __init__(self, **kwargs):
        # Create class-level logger.
        self.logger = loggers.create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get(str("logger_level"), str("DEBUG"))
        )

    @staticmethod
    def read_file_multipart(request):

        file_uploaded = request.get_param("file")
        file_obj = file_uploaded.file
        file_name = file_uploaded.filename

        return file_obj, file_name

    @staticmethod
    def read_file_raw(request):

        file_content = request.stream.read()

        file_obj = io.StringIO()
        file_obj.write(file_content.decode())
        file_obj.seek(0)

        file_name = ""

        return file_obj, file_name

    def read_uploaded_file(self, request):

        try:
            if request.get_param("file"):
                file_obj, file_name = self.read_file_multipart(request=request)
            else:
                file_obj, file_name = self.read_file_raw(request=request)
        except Exception as exc:
            msg_fmt = "Could not upload file."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="FileUploadFailure",
                description=msg_fmt + " Exception: {0}.".format(exc.message)
            )

        try:
            # (Ensure we can) read the file content.
            file_content = file_obj.read()
            # Rewind the file so it can be read by the `unicodecsv` package.
            file_obj.seek(0)
        except Exception as exc:
            msg = "Could not read content of uploaded file '{0}'."
            msg_fmt = msg.format(file_name)
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="InvalidFileUploaded",
                description=msg_fmt + " Exception: {0}.".format(exc.message)
            )

        return file_name, file_content, file_obj

    def prepare_response(self, response, results):

        try:
            response_json = ujson.dumps(results)
        except Exception as exc:
            msg = "Could not encode results '{0}' into JSON."
            msg_fmt = msg.format(results)
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_500,
                title="UnhandledError",
                description=msg_fmt + " Exception: {0}.".format(exc.message)
            )

        response.content_type = "application/json"
        response.body = response_json

        return response

    def read_csv_entries(self, file_name, file_obj):

        try:
            reader = unicodecsv.DictReader(
                csvfile=file_obj,
                fieldnames=["name", "email"]
            )
            entries = []
            for entry in reader:
                if entry["name"] == "name" or entry["email"] == "email":
                    continue

                entries.append(entry)

            return entries
        except Exception as exc:
            msg_fmt = "Could not read uploaded file '{0}'.".format(file_name)
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="InvalidRequest",
                description=msg_fmt + " Exception: {0}.".format(exc.message)
            )

    def execute(self, request, response):

        msg_fmt = "Processing 'upload_csv' request."
        self.logger.info(msg_fmt)

        file_name, file_content, file_obj = self.read_uploaded_file(
            request=request
        )

        msg_fmt = "Processing CSV file '{0}'.".format(file_name)
        self.logger.info(msg_fmt)

        entries = self.read_csv_entries(file_name=file_name, file_obj=file_obj)

        msg = "Processed CSV file '{0}' yielded {1} entries."
        msg_fmt = msg.format(file_name, len(entries))
        self.logger.info(msg_fmt)

        response = self.prepare_response(response=response, results=entries)

        return response

    def on_post(self, request, response):
        return self.execute(request=request, response=response)
