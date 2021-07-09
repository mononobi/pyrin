# -*- coding: utf-8 -*-
"""
swagger tags base module.
"""

from pyrin.api.swagger.interface import AbstractTag


class BaseTag(AbstractTag):
    """
    base tag class.
    """

    def __init__(self, *args, **options):
        """
        initializes an instance of BaseTag.

        :param object args: constructor arguments.
        """

        super().__init__()
