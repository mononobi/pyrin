# -*- coding: utf-8 -*-
"""
router package.
"""

from pyrin.packaging.base import Package


class RouterPackage(Package):
    """
    router package class.
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
