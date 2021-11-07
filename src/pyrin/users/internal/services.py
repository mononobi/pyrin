# -*- coding: utf-8 -*-
"""
users internal services module.
"""

from pyrin.application.services import get_component
from pyrin.users.internal import InternalUsersPackage


def get(id, *columns, **options):
    """
    gets the internal user with given id.

    :param int id: internal user id to be get.

    :param CoreColumn columns: columns to be fetched.
                               if not provided all columns will be fetched.

    :raises InternalUserNotFoundError: internal user not found error.

    :rtype: InternalUserEntity | ROW_RESULT
    """

    return get_component(InternalUsersPackage.COMPONENT_NAME).get(id, *columns, **options)


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


def get_login_user(username, password, *columns, **options):
    """
    gets an internal user with given username and password for logging in.

    it may return None if no internal user found.

    :param str username: username.
    :param str password: password.

    :param CoreColumn columns: columns to be fetched.
                               if not provided all columns will be fetched.

    :rtype: InternalUserEntity | ROW_RESULT
    """

    return get_component(InternalUsersPackage.COMPONENT_NAME).get_login_user(username, password,
                                                                             *columns, **options)


def update_last_login_at(id, **options):
    """
    updates the last login at for given user to current datetime.

    :param int id: internal user id to update its last login at.

    :raises InternalUserNotFoundError: internal user not found error.
    """

    return get_component(InternalUsersPackage.COMPONENT_NAME).update_last_login_at(id, **options)
