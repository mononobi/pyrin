# -*- coding: utf-8 -*-
"""
packaging base module.
"""

from pyrin.context import CoreObject


class Package(CoreObject):
    """
    base package class.
    all application python packages should be subclassed from this.
    except the application and packaging package itself that should not have Package.
    """

    # the name of the package.
    # example: `pyrin.application`.
    NAME = __name__

    # list of all packages that this package is dependent
    # on them and should be loaded after all of them.
    # example: ['pyrin.logging', 'pyrin.config']
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
