# -*- coding: utf-8 -*-
"""
users internal services module.
"""

from pyrin.application.services import get_component
from pyrin.users.internal import InternalUsersPackage


def is_active(id, **options):
    """
    gets a value indicating that given internal user is active.

    :param int id: internal user id to check its active status.

    :raises InternalUserNotFoundError: internal user not found error.

    :rtype: bool
    """

    return get_component(InternalUsersPackage.COMPONENT_NAME).is_active(id, **options)


def create(username, password, confirm_password, first_name, last_name, **options):
    """
    creates a new internal user based on given inputs.

    :param str username: username.
    :param str password: password.
    :param str confirm_password: confirm password.
    :param str first_name: first name.
    :param str last_name: last name.

    :keyword str mobile: mobile number.
    :keyword str email: email address.
    :keyword int gender: gender.
    :enum gender:
        FEMALE = 0
        MALE = 1
        OTHER = 2

    :keyword bool is_active: is active user.
    :keyword bool is_superuser: is superuser.

    :raises PasswordsDoNotMatchError: passwords do not match error.
    """

    return get_component(InternalUsersPackage.COMPONENT_NAME).create(username, password,
                                                                     confirm_password,
                                                                     first_name, last_name,
                                                                     **options)


def update(id, **options):
    """
    updates the given internal user based on given inputs.

    :param int id: internal user id.

    :keyword str username: username.
    :keyword str password: password.
    :keyword str confirm_password: confirm password.
    :keyword str first_name: first name.
    :keyword str last_name: last name.
    :keyword str mobile: mobile number.
    :keyword str email: email address.
    :keyword int gender: gender.
    :enum gender:
        FEMALE = 0
        MALE = 1
        OTHER = 2

    :keyword bool is_active: is active user.
    :keyword bool is_superuser: is superuser.

    :raises PasswordsDoNotMatchError: passwords do not match error.
    """

    return get_component(InternalUsersPackage.COMPONENT_NAME).update(id, **options)
