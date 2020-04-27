# -*- coding: utf-8 -*-
"""
mimetype handlers html module.
"""

import re

from pyrin.processor.mimetype.decorators import mimetype_handler
from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.processor.mimetype.handlers.base import MIMETypeHandlerBase


@mimetype_handler()
class HTMLMIMETypeHandler(MIMETypeHandlerBase):
    """
    html mimetype handler class.

    this class detects html markup in most inclusive way. it's not a
    real html parser. it just provides a way to detect if a string
    has potential html markup inside it.
    """

    # matches the html inside string.
    # matching is case-insensitive.
    HTML_REGEX = re.compile(r'^.*<.*\S+.*>.*', re.IGNORECASE | re.MULTILINE | re.DOTALL)

    def __init__(self, **options):
        """
        creates an instance of HTMLMIMETypeHandler.
        """

        super().__init__(**options)

    def _mimetype(self, value, **options):
        """
        gets the mimetype of given value.

        returns None if it fails to detect the mimetype.

        :param str value: value to detect its mimetype.

        :rtype: str
        """

        if self.HTML_REGEX.match(value.strip()):
            return MIMETypeEnum.HTML

        return None

    @property
    def accepted_type(self):
        """
        gets the accepted type for this mimetype handler.

        which could detect mimetype from this type.

        :rtype: type[str]
        """

        return str
