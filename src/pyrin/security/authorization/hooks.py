# -*- coding: utf-8 -*-
"""
authorization hooks module.
"""

import pyrin.security.authorization.services as authorization_services

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

        authorization_services.validate_authorizers()
