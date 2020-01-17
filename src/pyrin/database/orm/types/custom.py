# -*- coding: utf-8 -*-
"""
database orm types custom module.
"""

import uuid

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID


class GUID(TypeDecorator):
    """
    guid type class.

    it's a platform-independent guid type.
    uses postgresql's UUID type or mssql's UNIQUEIDENTIFIER
    type, otherwise uses CHAR(32), storing as stringified hex values.
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
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        """
        receive a bound parameter value to be converted.

        :param UUID value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :rtype: str
        """

        if value is None:
            return value
        elif dialect.name in ('postgresql', 'mssql'):
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hex string
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        """
        receive a result-row column value to be converted.

        :param str value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :rtype: UUID
        """

        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
