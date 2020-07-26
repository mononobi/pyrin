# -*- coding: utf-8 -*-
"""
packaging hooks module.
"""

from pyrin.core.structs import Hook


class PackagingHookBase(Hook):
    """
    packaging hook base class.

    all packages that need to be hooked into packaging business must
    implement this class and register it in packaging hooks.
    """

    def after_packages_loaded(self):
        """
        this method will be called after all application packages have been loaded.
        """
        pass

    def package_loaded(self, package_name, **options):
        """
        this method will be called after each application package has been loaded.

        :param str package_name: name of the loaded package.
        """
        pass
