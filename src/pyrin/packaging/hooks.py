# -*- coding: utf-8 -*-
"""
packaging hooks module.
"""

from pyrin.core.context import Hook


class PackagingHookBase(Hook):
    """
    packaging hook base class.
    all packages that need to be hooked into packaging business must
    implement this class and register it in packaging hooks.
    """

    def __init__(self):
        """
        initializes an instance of PackagingHookBase.
        """

        super().__init__()

    def after_packages_loaded(self):
        """
        this method will be called after all application packages has been loaded.
        """
        pass
