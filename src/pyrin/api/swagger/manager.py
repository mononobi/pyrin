# -*- coding: utf-8 -*-
"""
swagger manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.api.swagger.structs import ExtendedSwagger
from pyrin.application.services import get_current_app
from pyrin.api.swagger import SwaggerPackage
from pyrin.core.structs import Manager


class SwaggerManager(Manager):
    """
    swagger manager class.
    """

    package_class = SwaggerPackage

    def __init__(self):
        """
        initializes an instance of SwaggerManager.
        """

        super().__init__()

        self._swagger = None
        if self._is_enabled() is True:
            self._swagger = ExtendedSwagger(get_current_app(),
                                            config=self._get_configs(),
                                            merge=True)

    def _is_enabled(self):
        """
        gets a value indicating that swagger ui is enabled.

        :rtype: bool
        """

        return config_services.get_active('swagger', 'enabled')

    def _get_configs(self):
        """
        gets configuration from `swagger` config store.

        :rtype: dict
        """

        return config_services.get_active_section('swagger')
