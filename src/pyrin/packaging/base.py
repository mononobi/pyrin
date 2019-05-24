# -*- coding: utf-8 -*-
"""
packaging base module.
"""

from pyrin.core.context import CoreObject


class Package(CoreObject):
    """
    base package class.
    all application python packages should be subclassed from this.
    except the `application` and `packaging` packages that should not
    implement Package class.
    """

    # the name of the package.
    # example: `pyrin.api`.
    # should get it from __name__ for each package.
    NAME = None

    # list of all packages that this package is dependent
    # on them and should be loaded after all of them.
    # example: ['pyrin.logging', 'pyrin.config']
    # notice that all dependencies on `pyrin.application`
    # and `pyrin.packaging` should not be added to this list
    # because those two packages will be loaded at the beginning
    # and are always available before any other package gets loaded.
    DEPENDS = []
