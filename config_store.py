# -*- coding: utf-8 -*-
"""
Manages loaded server configurations.
"""

from bshop.core.base import ObjectBase


class ConfigStore(ObjectBase):
    """
    Keeps loaded server configurations.
    """

    def __init__(self):
        ObjectBase.__init__(self)
