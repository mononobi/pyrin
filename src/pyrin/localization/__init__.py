# -*- coding: utf-8 -*-
"""
localization package.
"""

import pyrin.application.services as application_services

from pyrin.packaging.context import Package


class LocalizationPackage(Package):
    """
    localization package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    COMPONENT_NAME = 'localization.component'
    CONFIG_STORE_NAMES = ['localization']

    def _load_configs(self, config_services):
        """
        loads all required configs of this package.
        this method is intended for overriding by
        subclasses to do custom configurations.

        :param Module config_services: configuration services dependency.
                                       to be able to overcome circular dependency problem,
                                       we should inject configuration services dependency
                                       into this method. because all other packages are
                                       referenced `packaging.context` module in them, so we
                                       can't import `pyrin.configuration.services` in this
                                       module. this is more beautiful in comparison to
                                       importing it inside this method.
        """

        flat_configs = config_services.get_all('localization')
        application_services.configure(flat_configs)
