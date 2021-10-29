# -*- coding: utf-8 -*-
"""
authentication hooks module.
"""

import pyrin.security.authentication.services as authentication_services

from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def after_packages_loaded(self):
        """
        this method will be called after all application packages have been loaded.
        """

        authentication_services.validate_authenticators()
