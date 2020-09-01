# -*- coding: utf-8 -*-
"""
users structs module.
"""

from pyrin.caching.structs import CacheableDict


class UserDTO(CacheableDict):
    """
    user dto class.

    this is a helper class that could be used as user info holder.
    if the user info is of dict type, it will be saved in current
    request with this type to be cacheable.
    """
    pass
