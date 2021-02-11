# -*- coding: utf-8 -*-
"""
orm types custom module.
"""

import uuid

from sqlalchemy.types import CHAR
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID

from pyrin.database.orm.types.base import CoreCustomType


class GUID(CoreCustomType):
    """
    guid type class.

    it's a platform-independent guid type.
    uses postgresql's UUID type or mssql's UNIQUEIDENTIFIER
    type, otherwise uses CHAR(36), storing as stringified hex values.
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        """
        returns a `TypeEngine` object corresponding to a dialect.

        :param Dialect dialect: the dialect in use.

        :rtype: TypeEngine
        """

        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        elif dialect.name == 'mssql':
            return dialect.type_descriptor(UNIQUEIDENTIFIER())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        """
        receive a bound parameter value to be converted.

        :param TypeEngine value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :rtype: str
        """

        if value is None:
            return value
        elif dialect.name in ('postgresql', 'mssql'):
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        """
        receive a result-row column value to be converted.

        :param str value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :rtype: uuid.UUID
        """

        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

    def compare_against_backend(self, dialect, conn_type):
        """
        returns True if this type is the same as the given database type,
        or None to allow the default implementation to compare these
        types. a return value of False means the given type does not
        match this type.

        :param Dialect dialect: the dialect in use.
        :param TypeEngine conn_type: type of the returned value from database.

        :rtype: bool
        """

        if dialect.name == 'postgresql':
            return isinstance(conn_type, UUID)
        elif dialect.name == 'mssql':
            return isinstance(conn_type, UNIQUEIDENTIFIER)
        else:
            return isinstance(conn_type, CHAR)
