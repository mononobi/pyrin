# -*- coding: utf-8 -*-
"""
database hooks module.
"""

import pyrin.database.services as database_services

from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def __init__(self):
        """
        initializes an instance of PackagingHook.
        """

        PackagingHookBase.__init__(self)

    def after_packages_loaded(self):
        """
        this method will be called after all application packages has been loaded.
        """

        # we have to configure session factories after all models have
        # been loaded to enable multiple database connections if needed.
        database_services.configure_session_factories()
