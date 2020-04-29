# -*- coding: utf-8 -*-
"""
mimetype handlers json module.
"""

import re

from pyrin.processor.mimetype.decorators import mimetype_handler
from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.processor.mimetype.handlers.base import MIMETypeHandlerBase


@mimetype_handler()
class JSONMIMETypeHandler(MIMETypeHandlerBase):
    """
    json mimetype handler class.
    """

    def __init__(self, **options):
        """
        creates an instance of JSONMIMETypeHandler.
        """

        super().__init__(**options)

    def _mimetype(self, value, **options):
        """
        gets the mimetype of given value.

        returns None if it fails to detect the mimetype.

        :param dict value: value to detect its mimetype.

        :rtype: str
        """

        return MIMETypeEnum.JSON

    @property
    def accepted_type(self):
        """
        gets the accepted type for this mimetype handler.

        which could detect mimetype from this type.

        :rtype: type[dict]
        """

        return dict


@mimetype_handler()
class JSONStringMIMETypeHandler(MIMETypeHandlerBase):
    """
    json string mimetype handler class.
    """

    # matches the json inside string.
    # matching is case-insensitive.
    JSON_REGEX = re.compile(r'^[ ]*\{.*\}[ ]*', re.IGNORECASE | re.MULTILINE | re.DOTALL)

    def _mimetype(self, value, **options):
        """
        gets the mimetype of given value.

        returns None if it fails to detect the mimetype.

        :param str value: value to detect its mimetype.

        :rtype: str
        """

        if self.JSON_REGEX.match(value.strip()):
            return MIMETypeEnum.JSON

        return None

    @property
    def accepted_type(self):
        """
        gets the accepted type for this mimetype handler.

        which could detect mimetype from this type.

        :rtype: type[str]
        """

        return str
