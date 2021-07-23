# -*- coding: utf-8 -*-
"""
session enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class RequestContextEnum(CoreEnum):
    """
    request context enum.
    """

    PAGINATOR = 'paginator'
    RESULT_SCHEMA = 'result_schema'
