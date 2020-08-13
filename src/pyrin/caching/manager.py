# -*- coding: utf-8 -*-
"""
caching manager module.
"""

from pyrin.caching import CachingPackage
from pyrin.core.structs import Manager


class CachingManager(Manager):
    """
    caching manager class.
    """

    package_class = CachingPackage
