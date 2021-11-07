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


def try_get_admin_page(entity):
    """
    gets the admin page for given entity class.

    it returns None if admin page does not exist.

    :param type[pyrin.database.model.base.BaseEntity] entity: the entity class of
                                                              admin page to be get.

    :rtype: pyrin.admin.interface.AbstractAdminPage
    """

    return get_component(AdminPackage.COMPONENT_NAME).try_get_admin_page(entity)


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

    :raises AdminOperationNotAllowedError: admin operation not allowed error.
    :raises EntityNotFoundError: entity not found error.

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

    :raises AdminOperationNotAllowedError: admin operation not allowed error.

    :rtype: object
    """

    return get_component(AdminPackage.COMPONENT_NAME).create(register_name, **data)


def update(register_name, pk, **data):
    """
    performs update on given admin page.

    :param str register_name: register name of admin page.
    :param object pk: entity primary key to be updated.

    :keyword **data: all data to be passed to related admin page for data creation.

    :raises AdminOperationNotAllowedError: admin operation not allowed error.
    :raises EntityNotFoundError: entity not found error.
    """

    return get_component(AdminPackage.COMPONENT_NAME).update(register_name, pk, **data)


def remove(register_name, pk):
    """
    performs remove on given admin page.

    :param str register_name: register name of admin page.
    :param object pk: entity primary key to be removed.

    :raises AdminOperationNotAllowedError: admin operation not allowed error.
    """

    return get_component(AdminPackage.COMPONENT_NAME).remove(register_name, pk)


def remove_bulk(register_name, pk):
    """
    performs remove bulk on given admin page.

    :param str register_name: register name of admin page.
    :param object | list[object] pk: entity primary keys to be removed.

    :raises AdminOperationNotAllowedError: admin operation not allowed error.
    """

    return get_component(AdminPackage.COMPONENT_NAME).remove_bulk(register_name, pk)


def remove_all(register_name):
    """
    performs remove all on given admin page.

    :param str register_name: register name of admin page.

    :raises AdminOperationNotAllowedError: admin operation not allowed error.
    """

    return get_component(AdminPackage.COMPONENT_NAME).remove_all(register_name)


def populate_main_metadata():
    """
    populates all admin pages main metadata.
    """

    return get_component(AdminPackage.COMPONENT_NAME).populate_main_metadata()


def get_main_metadata():
    """
    gets all admin pages main metadata.

    :raises AdminPagesHaveNotLoadedError: admin pages have not loaded error.

    :returns: dict(list pages,
                   dict configs)
    :rtype: dict
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


def register_name_for(entity):
    """
    gets the admin page register name for given entity class.

    it raises an error if the given entity does not have an admin page.

    :param type[pyrin.database.model.base.BaseEntity] entity: the entity class of
                                                              admin page to get its
                                                              register name.

    :raises AdminPageNotFoundError: admin page not found error.

    :rtype: str
    """

    return get_component(AdminPackage.COMPONENT_NAME).register_name_for(entity)


def url_for(register_name):
    """
    gets the base url for given admin page.

    :param str register_name: admin page register name.

    :rtype: str
    """

    return get_component(AdminPackage.COMPONENT_NAME).url_for(register_name)


def get_list_field_type(form_field_type):
    """
    gets the equivalent list field type for given form field type.

    it may return None.

    :param str form_field_type: form field type to get its list field type.
    :enum form_field_type:
        BOOLEAN = 'boolean'
        DATE = 'date'
        DATETIME = 'datetime'
        TIME = 'time'
        EMAIL = 'email'
        FILE = 'file'
        NUMBER = 'number'
        PASSWORD = 'password'
        TELEPHONE = 'telephone'
        STRING = 'string'
        TEXT = 'text'
        URL = 'url'
        UUID = 'uuid'
        IPV4 = 'ipv4'
        IPV6 = 'ipv6'
        OBJECT = 'object'

    :rtype: str
    """

    return get_component(AdminPackage.COMPONENT_NAME).get_list_field_type(form_field_type)


def populate_caches():
    """
    populates required caches of all registered admin pages.

    :returns: count of registered admin pages
    :rtype: int
    """

    return get_component(AdminPackage.COMPONENT_NAME).populate_caches()


def get_configs():
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

    return get_component(AdminPackage.COMPONENT_NAME).get_configs()


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

    return get_component(AdminPackage.COMPONENT_NAME).login(username, password, **options)
