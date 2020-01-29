# -*- coding: utf-8 -*-
"""
session services module.
"""

from pyrin.application.services import get_component
from pyrin.security.session import SessionPackage


def get_current_user():
    """
    gets current user.
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_current_user()


def set_current_user(user):
    """
    sets current user.

    :param user: user object.

    :raises InvalidUserError: invalid user error.
    :raises CouldNotOverwriteCurrentUserError: could not overwrite current user error.
    """

    return get_component(SessionPackage.COMPONENT_NAME).set_current_user(user)


def get_current_request():
    """
    gets current request object.

    :raises RuntimeError: runtime error.

    :rtype: CoreRequest
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_current_request()


def get_current_request_context():
    """
    gets current request context.

    :rtype: dict
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_current_request_context()


def add_request_context(key, value):
    """
    adds the given key/value pair into current request context.

    :param str key: key to be added.
    :param object value: value to be added.

    :raises InvalidRequestContextKeyNameError: invalid request context key name error.
    """

    return get_component(SessionPackage.COMPONENT_NAME).add_request_context(key, value)


def is_fresh():
    """
    gets a value indicating that current request has a fresh token.
    fresh token means a token which created upon providing user credentials
    to server, not using a refresh token.

    :rtype: bool
    """

    return get_component(SessionPackage.COMPONENT_NAME).is_fresh()


def get_current_token_payload():
    """
    gets current request's token payload.

    :rtype: dict
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_current_token_payload()


def get_current_token_header():
    """
    gets current request's token header.

    :rtype: dict
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_current_token_header()


def set_component_custom_key(value):
    """
    sets the component custom key.

    :param object value: component custom key value.

    :raises InvalidComponentCustomKeyError: invalid component custom key error.
    """

    return get_component(SessionPackage.COMPONENT_NAME).set_component_custom_key(value)


def get_component_custom_key():
    """
    gets component custom key.

    :rtype: object
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_component_custom_key()


def get_safe_current_request():
    """
    gets current request object in a safe manner.
    meaning that if the request does not exist in current context, it will
    return a None object instead of raising an error.

    :rtype: CoreRequest
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_safe_current_request()


def get_safe_current_user():
    """
    gets current user in a safe manner.
    meaning that if the request does not exist in current context, it will
    return a None object instead of raising an error.
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_safe_current_user()


def is_request_context_available():
    """
    gets a value indicating that request context is available for usage.

    :rtype: bool
    """

    return get_component(SessionPackage.COMPONENT_NAME).is_request_context_available()
