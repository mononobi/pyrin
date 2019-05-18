# -*- coding: utf-8 -*-
"""
configuration manager module.
"""

from pyrin.context import CoreObject


class ConfigurationManager(CoreObject):
    """
    configuration manager class.
    """

    def __init__(self, **options):
        """
        initializes an instance of ConfigurationManager.

        :keyword str configs_directory: the absolute path to the configs directory.
                                        example configs_directory =
                                        `/var/app_root/pyrin/settings/configs`
        """

        CoreObject.__init__(self)

        self._configs_directory = options.get('configs_directory', None)
