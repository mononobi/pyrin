# -*- coding: utf-8 -*-
"""
database package.
"""

from pyrin.packaging.base import Package


class DatabasePackage(Package):
    """
    database package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.converters',
               'pyrin.api']

    def load(self):
        """
        loads the package and it's configs.
        """

        self._load_configs()

    def _load_configs(self):
        """
        loads the package required configs.
        """
