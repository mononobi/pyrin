# -*- coding: utf-8 -*-
"""
swagger tags base module.
"""

from pyrin.api.swagger.interface import AbstractTag
from pyrin.api.swagger.tags.exceptions import TagNameIsRequiredError, TagIsRequiredError


class BaseTag(AbstractTag):
    """
    base tag class.
    """

    def __init__(self, *args, **options):
        """
        initializes an instance of BaseTag.

        :param object args: constructor arguments.

        :raises TagNameIsRequiredError: tag name is required error.
        :raises TagIsRequiredError: tag is required error.
        """

        if self._name in (None, ''):
            raise TagNameIsRequiredError('Name is required for tag [{instance}].'
                                         .format(instance=self))

        if self._tag in (None, ''):
            raise TagIsRequiredError('Tag is required for tag [{instance}].'
                                     .format(instance=self))

        super().__init__()
