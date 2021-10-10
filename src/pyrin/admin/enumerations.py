# -*- coding: utf-8 -*-
"""
admin enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class ListFieldTypeEnum(CoreEnum):
    """
    list field type enum.
    """

    BOOLEAN = 'boolean'
    NUMERIC = 'numeric'
    DATE = 'date'
    DATETIME = 'datetime'
    TIME = 'time'
    STRING = 'string'
    CURRENCY = 'currency'
    OBJECT = 'object'


class FormFieldTypeEnum(CoreEnum):
    """
    form field type enum.
    """

    BOOLEAN = 'boolean'
    DATE = 'date'
    DATETIME = 'datetime'
    TIME = 'time'
    EMAIL = 'email'
    FILE = 'file'
    NUMBER = 'number'
    INTEGER = 'integer'
    FLOAT = 'float'
    PASSWORD = 'password'
    TELEPHONE = 'telephone'
    STRING = 'string'
    TEXT = 'text'
    URL = 'url'
    UUID = 'uuid'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    OBJECT = 'object'
