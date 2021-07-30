# -*- coding: utf-8 -*-
"""
admin services module.
"""

from pyrin.application.services import get_component
from pyrin.admin import AdminPackage


def register(instance, **options):
    """
    registers the provided instance into available admin pages.

    :param pyrin.admin.interface.AbstractAdminPage instance: admin page instance.

    :keyword bool replace: specifies that if another admin page with the same name
                           or the same entity exists, replace it.
                           defaults to False if not provided and raises an error.

    :raises InvalidAdminPageTypeError: invalid admin page type error.
    :raises DuplicatedAdminPageError: duplicated admin page error.
    """

    return get_component(AdminPackage.COMPONENT_NAME).register(instance, **options)


def is_admin_enabled():
    """
    gets a value indicating that admin api is enabled.

    :rtype: bool
    """

    return get_component(AdminPackage.COMPONENT_NAME).is_admin_enabled()


def has_admin(entity):
    """
    gets a value indicating that given entity class has admin page.

    :param type[pyrin.database.model.base.BaseEntity] entity: entity class.

    :rtype: bool
    """

    return get_component(AdminPackage.COMPONENT_NAME).has_admin(entity)


def get_admin_base_url():
    """
    gets admin base url.

    :rtype: str
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_admin_base_url()


def get_admin_configurations():
    """
    gets the admin api configurations.

    :returns: dict(bool enabled: enable admin api,
                   bool authenticated: admin api access type,
                   str url: admin api base url)
    :rtype: dict
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_admin_configurations()


def get_default_category():
    """
    gets the default category to be used for admin pages without category.

    :rtype: str
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_default_category()


def get(register_name, pk):
    """
    gets an entity with given primary key.

    :param str register_name: register name of admin page.
    :param object pk: primary key of entity to be get.

    :rtype: pyrin.database.model.base.BaseEntity
    """

    return get_component(AdminPackage.COMPONENT_NAME).get(register_name, pk)


def find(register_name, **filters):
    """
    performs find on given admin page and returns the result.

    :param str register_name: register name of admin page.

    :keyword **filters: all filters to be passed to related admin page.

    :rtype: list[ROW_RESULT]
    """

    return get_component(AdminPackage.COMPONENT_NAME).find(register_name, **filters)


def create(register_name, **data):
    """
    performs create on given admin page.

    :param str register_name: register name of admin page.

    :keyword **data: all data to be passed to related admin page for data creation.
    """

    return get_component(AdminPackage.COMPONENT_NAME).create(register_name, **data)


def update(register_name, pk, **data):
    """
    performs update on given admin page.

    :param str register_name: register name of admin page.
    :param object pk: entity primary key to be updated.

    :keyword **data: all data to be passed to related admin page for data creation.
    """

    return get_component(AdminPackage.COMPONENT_NAME).update(register_name, pk, **data)


def remove(register_name, pk):
    """
    performs remove on given admin page.

    :param str register_name: register name of admin page.
    :param object pk: entity primary key to be removed.
    """

    return get_component(AdminPackage.COMPONENT_NAME).remove(register_name, pk)


def populate_main_metadata():
    """
    populates all admin pages main metadata.
    """

    return get_component(AdminPackage.COMPONENT_NAME).populate_main_metadata()


def get_main_metadata():
    """
    gets all admin pages main metadata.

    :raises AdminPagesHaveNotLoadedError: admin pages have not loaded error.

    :rtype: list[dict]
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_main_metadata()


def get_find_metadata(register_name):
    """
    gets the find metadata for given admin page.

    :param str register_name: register name of admin page.

    :rtype: dict
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_find_metadata(register_name)


def get_create_metadata(register_name):
    """
    gets the create metadata for given admin page.

    :param str register_name: register name of admin page.

    :rtype: dict
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_create_metadata(register_name)


def get_update_metadata(register_name):
    """
    gets the update metadata for given admin page.

    :param str register_name: register name of admin page.

    :rtype: dict
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_update_metadata(register_name)


def url_for(register_name):
    """
    gets the base url for given admin page.

    :param str register_name: admin page register name.

    :rtype: str
    """

    return get_component(AdminPackage.COMPONENT_NAME).url_for(register_name)
