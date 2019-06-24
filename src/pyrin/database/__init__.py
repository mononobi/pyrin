# -*- coding: utf-8 -*-
"""
database package.
"""

from pyrin.database.utils.pool import get_pool_class
from pyrin.packaging.context import Package


class DatabasePackage(Package):
    """
    database package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration',
               'pyrin.security.session',
               'pyrin.logging']

    COMPONENT_NAME = 'database.component'
    CONFIG_STORE_NAMES = ['database']

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

        database_configs = config_services.get_active_section('database')
        pool_name = database_configs['sqlalchemy_poolclass']
        pool_class = get_pool_class(pool_name)
        database_configs.update(sqlalchemy_poolclass=pool_class)
