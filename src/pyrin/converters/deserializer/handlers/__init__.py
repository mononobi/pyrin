# -*- coding: utf-8 -*-
"""
deserializer handlers package.
"""

from pyrin.packaging.base import Package


class DeserializerHandlersPackage(Package):
    """
    deserializer handlers package class.
    """

    NAME = __name__
    DEPENDS = []

    def load(self):
        """
        loads the package and it's configs.
        """

        self._load_configs()

    def _load_configs(self):
        """
        loads the package required configs.
        """
