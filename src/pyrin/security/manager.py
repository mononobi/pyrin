# -*- coding: utf-8 -*-
"""
security manager module.
"""

from pyrin.core.context import CoreObject


class SecurityManager(CoreObject):
    """
    security manager class.
    this class is intended to be an interface for top level application's security
    package, so most methods of this class will raise CoreNotImplementedError.
    """

    def create_user(self, username, encrypted_password, **options):
        pass