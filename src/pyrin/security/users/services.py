# -*- coding: utf-8 -*-
"""
users services module.
"""

from pyrin.application.services import get_component
from pyrin.security.users import UsersPackage


def is_active(user, **options):
    """
    gets a value indicating that given user is active.

    :param user: user to check its active status.

    :rtype: bool
    """

    return get_component(UsersPackage.COMPONENT_NAME).is_active(user, **options)
