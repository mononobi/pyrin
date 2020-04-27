# -*- coding: utf-8 -*-
"""
mimetype enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class MIMETypeEnum(CoreEnum):
    """
    mimetype enum.
    """

    TEXT = 'text/plain'
    HTML = 'text/html'
    JAVASCRIPT = 'text/javascript'
    OCTET_STREAM = 'application/octet-stream'
    JSON = 'application/json'
