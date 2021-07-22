# -*- coding: utf-8 -*-
"""
admin api module.
"""

import pyrin.admin.services as admin_services

from pyrin.api.router.decorators import api, post, patch, delete


admin_config = admin_services.get_admin_configurations()
admin_config.update(swagger=False)
admin_config.pop('paged', None)
is_enabled = admin_config.pop('enabled', True)
url = admin_config.pop('url', '/admin')

if is_enabled is True:
    @api(f'{url}/<register_name>', **admin_config, paged=True)
    def find(register_name, **filters):
        """
        performs find on given admin page and returns the result.

        :param str register_name: register name of admin page.

        :keyword **filters: all filters to be passed to related admin page.

        :rtype: list[ROW_RESULT]
        """

        return admin_services.find(register_name, **filters)


    @post(f'{url}/<register_name>', **admin_config)
    def create(register_name, **data):
        """
        performs create on given admin page.

        :param str register_name: register name of admin page.

        :keyword **data: all data to be passed to related admin page for data creation.
        """

        return admin_services.create(register_name, **data)


    @patch(f'{url}/<register_name>/<pk>', **admin_config)
    def update(register_name, pk, **data):
        """
        performs update on given admin page.

        :param str register_name: register name of admin page.
        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related admin page for data creation.
        """

        return admin_services.update(register_name, pk, **data)


    @delete(f'{url}/<register_name>/<pk>', **admin_config)
    def remove(register_name, pk, **options):
        """
        performs remove on given admin page.

        :param str register_name: register name of admin page.
        :param object pk: entity primary key to be removed.
        """

        return admin_services.remove(register_name, pk)
