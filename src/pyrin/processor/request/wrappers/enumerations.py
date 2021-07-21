# -*- coding: utf-8 -*-
"""
request wrappers enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class DeserializationTypeEnum(CoreEnum):
    """
    deserialization type enum.
    """

    FORM_DATA = 'form data'
    QUERY_STRINGS = 'query strings'
    URL_PARAMS = 'url params'
