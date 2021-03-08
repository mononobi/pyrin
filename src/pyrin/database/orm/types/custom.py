# -*- coding: utf-8 -*-
"""
orm types custom module.
"""

import uuid

from sqlalchemy.types import CHAR
from sqlalchemy import TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from pyrin.database.enumerations import DialectEnum
from pyrin.database.orm.types.base import CoreCustomType
from pyrin.database.orm.types.mixin import DateTimeMixin


class GUID(CoreCustomType):
    """
    guid type class.

    it's a platform-independent guid type.
    uses postgresql's UUID type or mssql's UNIQUEIDENTIFIER
    type, otherwise uses CHAR(36), storing as stringified hex values.
    """

    impl = CHAR

    def _to_database(self, value, dialect):
        """
        converts given value to be emitted to database.

        :param object value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :rtype: str
        """

        if dialect.name in (DialectEnum.POSTGRESQL, DialectEnum.SQLSERVER):
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def _from_database(self, value, dialect):
        """
        converts given value to python type after fetching it from database.

        :param object value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :rtype: uuid.UUID
        """

        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)

        return value

    def _coerce_to_string(self, value, dialect):
        """
        coerces the given value to string before sending to database.

        :param object value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :rtype: str
        """

        return value

    def load_dialect_impl(self, dialect):
        """
        returns a `TypeEngine` object corresponding to a dialect.

        :param Dialect dialect: the dialect in use.

        :rtype: TypeEngine
        """

        if dialect.name == DialectEnum.POSTGRESQL:
            return dialect.type_descriptor(UUID())
        elif dialect.name == DialectEnum.SQLSERVER:
            return dialect.type_descriptor(UNIQUEIDENTIFIER())
        else:
            return dialect.type_descriptor(CHAR(36))

    def compare_against_backend(self, dialect, conn_type):
        """
        returns True if this type is the same as the given database type.

        or None to allow the default implementation to compare these
        types. a return value of False means the given type does not
        match this type.

        :param Dialect dialect: the dialect in use.
        :param TypeEngine conn_type: type of the returned value from database.

        :rtype: bool
        """

        if dialect.name == DialectEnum.POSTGRESQL:
            return isinstance(conn_type, UUID)
        elif dialect.name == DialectEnum.SQLSERVER:
            return isinstance(conn_type, UNIQUEIDENTIFIER)
        else:
            return isinstance(conn_type, CHAR)

    @property
    def python_type(self):
        """
        gets the python type object expected to be returned by instances of this type.

        :rtype: type[uuid.UUID]
        """

        return uuid.UUID


class CoreTimeStamp(DateTimeMixin):
    """
    core timestamp class.

    this is a helper type that will handle datetime values correctly on sqlite backend.
    on sqlite backend, the timezone of database will always considered as utc.
    it works as default on other backends.
    """

    impl = TIMESTAMP


class CoreDateTime(DateTimeMixin):
    """
    core datetime class.

    this is a helper type that will handle datetime values correctly on sqlite backend.
    on sqlite backend, the timezone of database will always considered as utc.
    it works as default on other backends.
    """

    impl = DateTime
