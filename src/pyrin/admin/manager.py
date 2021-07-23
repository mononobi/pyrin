# -*- coding: utf-8 -*-
"""
admin manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.core.globals import _
from pyrin.admin import AdminPackage
from pyrin.core.structs import Context, Manager
from pyrin.admin.interface import AbstractAdminPage
from pyrin.admin.exceptions import InvalidAdminPageTypeError, DuplicatedAdminPageError, \
    AdminPageNotFoundError, AdminOperationNotAllowedError


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

        # a dict containing all registered admin pages for different entity types.
        # in the form of:
        # {BaseEntity entity: AbstractAdminPage instance}
        self._admin_entities = Context()

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

    def _remove_from_pages(self, register_name):
        """
        removes the admin page with given register name from admin pages.

        it returns the removed admin page.

        :param str register_name: register name of the admin page to be removed.

        :rtype: pyrin.admin.interface.AbstractAdminPage
        """

        instance = self._admin_pages.pop(register_name, None)
        if instance is not None:
            return self._remove_from_entities(instance.get_entity())

        return instance

    def _remove_from_entities(self, entity):
        """
        removes the admin page with given entity from admin entities.

        it returns the removed admin page.

        :param pyrin.database.model.base.BaseEntity entity: the entity class of
                                                            admin page to be removed.

        :rtype: pyrin.admin.interface.AbstractAdminPage
        """

        instance = self._admin_entities.pop(entity, None)
        if instance is not None:
            return self._remove_from_pages(instance.get_register_name())

        return None

    def is_admin_enabled(self):
        """
        gets a value indicating that admin api is enabled.

        :rtype: bool
        """

        return config_services.get_active('admin', 'enabled')

    def has_admin(self, entity):
        """
        gets a value indicating that given entity class has admin page.

        :param type[pyrin.database.model.base.BaseEntity] entity: entity class.

        :rtype: bool
        """

        return entity in self._admin_entities

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

    def get_default_category(self):
        """
        gets the default category to be used for admin pages without category.

        :rtype: str
        """

        category = config_services.get_active('admin', 'default_category')
        return category.upper()

    def register(self, instance, **options):
        """
        registers the provided instance into available admin pages.

        :param pyrin.admin.interface.AbstractAdminPage instance: admin page instance.

        :keyword bool replace: specifies that if another admin page with the same name
                               or the same entity exists, replace it.
                               defaults to False if not provided and raises an error.

        :raises InvalidAdminPageTypeError: invalid admin page type error.
        :raises DuplicatedAdminPageError: duplicated admin page error.
        """

        if not isinstance(instance, AbstractAdminPage):
            raise InvalidAdminPageTypeError('Input parameter [{admin}] is '
                                            'not an instance of [{base}].'
                                            .format(admin=instance, base=AbstractAdminPage))

        replace = options.get('replace', False)
        if instance.get_register_name() in self._admin_pages:
            if replace is not True:
                raise DuplicatedAdminPageError('There is another registered admin page '
                                               'with register name [{name}] but "replace" '
                                               'option is not set, so admin page [{instance}] '
                                               'could not be registered.'
                                               .format(name=instance.get_register_name(),
                                                       instance=instance))

            self._remove_from_pages(instance.get_register_name())

        if instance.get_entity() in self._admin_entities:
            if replace is not True:
                raise DuplicatedAdminPageError('There is another registered admin page '
                                               'for entity [{entity}] but "replace" '
                                               'option is not set, so admin page [{instance}] '
                                               'could not be registered.'
                                               .format(entity=instance.get_entity(),
                                                       instance=instance))

            self._remove_from_entities(instance.get_entity())

        self._admin_pages[instance.get_register_name()] = instance
        self._admin_entities[instance.get_entity()] = instance

    def _get_admin_page(self, register_name):
        """
        gets the admin page with given register name.

        :param str register_name: register name of admin page to be get.
                                  this name is case-insensitive.

        :raises AdminPageNotFoundError: admin page not found error.

        :rtype: pyrin.admin.interface.AbstractAdminPage
        """

        name = str(register_name).lower()
        if name not in self._admin_pages:
            raise AdminPageNotFoundError(_('Admin page [{name}] not found.')
                                         .format(name=name))

        return self._admin_pages.get(name)

    def get(self, register_name, pk):
        """
        gets an entity with given primary key.

        :param str register_name: register name of admin page.
        :param object pk: primary key of entity to be get.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.

        :rtype: pyrin.database.model.base.BaseEntity
        """

        admin = self._get_admin_page(register_name)
        if not admin.has_get_permission():
            raise AdminOperationNotAllowedError(_('Admin page [{name}] does '
                                                  'not allow get operation.')
                                                .format(name=admin.get_register_name()))

        return admin.get(pk)

    def find(self, register_name, **filters):
        """
        performs find on given admin page and returns the result.

        :param str register_name: register name of admin page.

        :keyword **filters: all filters to be passed to related admin page.

        :rtype: list[ROW_RESULT]
        """

        admin = self._get_admin_page(register_name)
        return admin.find(**filters)

    def create(self, register_name, **data):
        """
        performs create on given admin page.

        :param str register_name: register name of admin page.

        :keyword **data: all data to be passed to related admin page for data creation.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        """

        admin = self._get_admin_page(register_name)
        if not admin.has_create_permission():
            raise AdminOperationNotAllowedError(_('Admin page [{name}] does '
                                                  'not allow create operation.')
                                                .format(name=admin.get_register_name()))

        return admin.create(**data)

    def update(self, register_name, pk, **data):
        """
        performs update on given admin page.

        :param str register_name: register name of admin page.
        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related admin page for data creation.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        """

        admin = self._get_admin_page(register_name)
        if not admin.has_get_permission():
            raise AdminOperationNotAllowedError(_('Admin page [{name}] does '
                                                  'not allow update operation.')
                                                .format(name=admin.get_register_name()))

        return admin.update(pk, **data)

    def remove(self, register_name, pk):
        """
        performs remove on given admin page.

        :param str register_name: register name of admin page.
        :param object pk: entity primary key to be removed.

        :raises AdminOperationNotAllowedError: admin operation not allowed error.
        """

        admin = self._get_admin_page(register_name)
        if not admin.has_get_permission():
            raise AdminOperationNotAllowedError(_('Admin page [{name}] does '
                                                  'not allow remove operation.')
                                                .format(name=admin.get_register_name()))

        return admin.remove(pk)
