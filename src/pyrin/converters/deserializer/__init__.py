# -*- coding: utf-8 -*-
"""
deserializer package.
"""

from pyrin.packaging.base import Package


class DeserializerPackage(Package):
    """
    deserializer package class.
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
