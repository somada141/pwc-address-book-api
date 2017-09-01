# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.dialects
import sqlalchemy.dialects.mysql

from .orm_base import Base, OrmBase


class Contact(Base, OrmBase):
    # set table name
    __tablename__ = "contacts"

    contact_id = sqlalchemy.Column(
        sqlalchemy.dialects.mysql.INTEGER(display_width=11, unsigned=True),
        nullable=False,
        primary_key=True
    )

    name = sqlalchemy.Column(
        sqlalchemy.dialects.mysql.VARCHAR(length=180),
        nullable=False
    )

    email = sqlalchemy.Column(
        sqlalchemy.dialects.mysql.VARCHAR(length=180),
        unique=True,
        nullable=False
    )
