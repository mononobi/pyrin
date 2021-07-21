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


def find(register_name, **filters):
    return get_component(AdminPackage.COMPONENT_NAME).find(register_name, **filters)
