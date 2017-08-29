# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from . import loggers
from . import sql
from . import schemata
from .orm_base import Base
from .orm import Contact
from . import excs


class TapPab(sql.BoilerplateSql):
    def __init__(
        self,
        sql_username,
        sql_password,
        sql_host,
        sql_port,
        sql_db,
        **kwargs
    ):
        super(TapPab, self).__init__(
            sql_username=sql_username,
            sql_password=sql_password,
            sql_host=sql_host,
            sql_port=sql_port,
            sql_db=sql_db,
            **kwargs
        )

        # create class-level self.logger
        self.logger = loggers.create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get(str("logger_level"), str("DEBUG"))
        )

        Base.metadata.create_all(self.engine)

    @schemata.validate_parameters()
    def get_contact_by_email(self, contact_email):
        with self.session_scope() as session:
            query = session.query(Contact)
            query = query.filter(Contact.email == contact_email)

            contact_obj = query.first()

        return contact_obj

    def get_contacts(self):

        with self.session_scope() as session:
            query = session.query(Contact)

            contact_objs = query.all()

        return contact_objs

    @schemata.validate_parameters()
    def has_contact_by_email(self, contact_email):

        contact_obj = self.get_contact_by_email(contact_email=contact_email)

        if contact_obj:
            return True

        return False

    @schemata.validate_parameters()
    def add_contact(self, contact_name, contact_email):

        if self.has_contact_by_email(contact_email=contact_email):
            msg = "Contact with email '{0}' already exists in database."
            msg_fmt = msg.format(contact_email)
            raise excs.RecordExists(msg_fmt)

        with self.session_scope() as session:
            contact_obj = Contact()
            contact_obj.email = contact_email
            contact_obj.name = contact_name
            contact_obj.added = contact_obj.updated = datetime.datetime.utcnow()

            session.add(contact_obj)

            session.flush([contact_obj])

        return contact_obj

    @schemata.validate_parameters()
    def update_contact_name(self, contact_email, contact_name):

        with self.session_scope() as session:
            contact_obj = self.get_contact_by_email(contact_email=contact_email)

            if contact_obj is None:
                msg = "No contact with email '{0}' found in database."
                msg_fmt = msg.format(contact_email)
                raise excs.RecordDoesNotExist(msg_fmt)

            contact_obj.name = contact_name
            contact_obj.updated = datetime.datetime.utcnow()

            session.merge(contact_obj)

        return contact_obj

