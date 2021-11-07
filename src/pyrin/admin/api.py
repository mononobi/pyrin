# -*- coding: utf-8 -*-
"""
admin api module.
"""

import pyrin.admin.services as admin_services

from pyrin.api.router.decorators import api, post, patch, delete


admin_config = admin_services.get_admin_configurations()
url = admin_services.get_admin_base_url()
admin_config.update(swagger=False)
admin_config.pop('paged', None)
admin_config.pop('readable', None)
admin_config.pop('url', None)
is_enabled = admin_config.pop('enabled', False)

if is_enabled is True:
    @api(f'{url}<register_name>/<pk>', **admin_config)
    def get(register_name, pk, **options):
        """
        gets an entity with given primary key.

        :param str register_name: register name of admin page.
        :param object pk: primary key of entity to be get.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        :raises EntityNotFoundError: entity not found error.

        :rtype: pyrin.database.model.base.BaseEntity
        """

        return admin_services.get(register_name, pk)


    @api(f'{url}<register_name>', **admin_config)
    def find(register_name, **filters):
        """
        performs find on given admin page and returns the result.

        :param str register_name: register name of admin page.

        :keyword **filters: all filters to be passed to related admin page.

        :rtype: list[ROW_RESULT]
        """

        return admin_services.find(register_name, **filters)


    @post(f'{url}<register_name>', **admin_config)
    def create(register_name, **data):
        """
        performs create on given admin page.

        :param str register_name: register name of admin page.

        :keyword **data: all data to be passed to related admin page for data creation.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.

        :rtype: object
        """

        return admin_services.create(register_name, **data)


    @patch(f'{url}<register_name>/<pk>', **admin_config)
    def update(register_name, pk, **data):
        """
        performs update on given admin page.

        :param str register_name: register name of admin page.
        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related admin page for data creation.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        :raises EntityNotFoundError: entity not found error.
        """

        return admin_services.update(register_name, pk, **data)


    @delete(f'{url}<register_name>/<pk>', **admin_config)
    def remove(register_name, pk, **options):
        """
        performs remove on given admin page.

        :param str register_name: register name of admin page.
        :param object pk: entity primary key to be removed.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        """

        return admin_services.remove(register_name, pk)


    @delete(f'{url}<register_name>/bulk', **admin_config)
    def remove_bulk(register_name, pk):
        """
        performs remove bulk on given admin page.

        :param str register_name: register name of admin page.
        :param object | list[object] pk: entity primary keys to be removed.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        """

        return admin_services.remove_bulk(register_name, pk)


    @delete(f'{url}<register_name>', **admin_config)
    def remove_all(register_name):
        """
        performs remove all on given admin page.

        :param str register_name: register name of admin page.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        """

        return admin_services.remove_all(register_name)


    @api(f'{url}metadata', **admin_config)
    def get_main_metadata(**options):
        """
        gets all admin pages main metadata.

        :raises AdminPagesHaveNotLoadedError: admin pages have not loaded error.

        :returns: dict(list pages,
                       dict configs)
        :rtype: dict
        """

        return admin_services.get_main_metadata()


    @api(f'{url}metadata/<register_name>/find', **admin_config)
    def get_find_metadata(register_name, **options):
        """
        gets the find metadata for given admin page.

        :param str register_name: register name of admin page.

        :rtype: dict
        """

        return admin_services.get_find_metadata(register_name)


    @api(f'{url}metadata/<register_name>/create', **admin_config)
    def get_create_metadata(register_name, **options):
        """
        gets the create metadata for given admin page.

        :param str register_name: register name of admin page.

        :rtype: dict
        """

        return admin_services.get_create_metadata(register_name)


    @api(f'{url}metadata/<register_name>/update', **admin_config)
    def get_update_metadata(register_name, **options):
        """
        gets the update metadata for given admin page.

        :param str register_name: register name of admin page.

        :rtype: dict
        """

        return admin_services.get_update_metadata(register_name)


    @api(f'{url}metadata/configs', **admin_config)
    def get_configs(**options):
        """
        gets the required configs of admin api.

        :returns: dict(str panel_name,
                       str page_key,
                       str page_size_key,
                       str ordering_key,
                       str locale_key,
                       str timezone_key,
                       str search_param,
                       str hidden_pk_name)
        :rtype: dict
        """

        return admin_services.get_configs()

    @post(f'{url}login', authenticated=False)
    def login(username, password, **options):
        """
        logs in an internal user with given info into admin panel.

        :param str username: username.
        :param str password: password.

        :raises ProvidedUsernameOrPasswordAreIncorrect: provided username or
                                                        password are incorrect.

        :returns: dict(str access_token)
        :rtype: dict
        """

        return admin_services.login(username, password, **options)
