# -*- coding: utf-8 -*-
"""
admin services module.
"""

from pyrin.application.services import get_component
from pyrin.admin import AdminPackage


def register(instance):
    return get_component(AdminPackage.COMPONENT_NAME).register(instance)


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
