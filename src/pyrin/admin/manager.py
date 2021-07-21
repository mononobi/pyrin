# -*- coding: utf-8 -*-
"""
admin manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.admin import AdminPackage
from pyrin.core.structs import Context, Manager


class AdminManager(Manager):
    """
    admin manager class.
    """

    package_class = AdminPackage

    def __init__(self, **options):
        """
        initializes an instance of AdminManager.
        """

        super().__init__()

        # a dict containing all registered admin pages in the form of:
        # {str register_name: AbstractAdminPage instance}
        self._admin_pages = Context()
        self._base_url = self._load_base_url()

    def _load_base_url(self):
        """
        loads admin base url from `admin` config store.

        :rtype: str
        """

        url = config_services.get_active('admin', 'url')
        if not url.endswith('/'):
            url = f'{url}/'

        return url

    def get_admin_base_url(self):
        """
        gets admin base url.

        :rtype: str
        """

        return self._base_url

    def get_admin_configurations(self):
        """
        gets the admin api configurations.

        :returns: dict(bool enabled: enable admin api,
                       bool authenticated: admin api access type,
                       str url: admin api base url)
        :rtype: dict
        """

        return config_services.get_active_section('admin')

    def register(self, instance):
        self._admin_pages[instance.register_name] = instance

    def find(self, register_name, **filters):
        admin = self._admin_pages[register_name]
        return admin.find(**filters)
