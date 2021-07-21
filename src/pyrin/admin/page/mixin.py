# -*- coding: utf-8 -*-
"""
admin page mixin module.
"""

from pyrin.caching.mixin.typed import TypedCacheMixin


class AdminPageCacheMixin(TypedCacheMixin):
    """
    admin page cache mixin class.

    this class adds caching support to its subclasses.
    """

    _container = {}
