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


def get_current_request_id():
    """
    gets current request id.

    this method is implemented to overcome the hash problem of requests.
    `CoreRequest` objects are hashable themselves, but when they used as a dict key
    some hash collisions will occur. so we have to expose the exact request id to
    be able to use it as a dict key in places such as database scoped sessions.

    :raises RuntimeError: runtime error.

    :rtype: uuid.UUID
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_current_request_id()


def add_request_context(key, value, **options):
    """
    adds the given key/value pair into current request context.

    :param str key: key name to be added.
    :param object value: value to be added.

    :keyword bool replace: specifies that if a key with the same name
                           is already present, replace it. otherwise
                           raise an error. defaults to False if not provided.

    :raises InvalidRequestContextKeyNameError: invalid request context key name error.
    :raises RequestContextKeyIsAlreadyPresentError: request context key is
                                                    already present error.
    """

    get_component(SessionPackage.COMPONENT_NAME).add_request_context(key, value, **options)


def get_request_context(key, default=None):
    """
    gets the value for given key from current request context.

    it gets the default value if key is not present in the request context.

    :param str key: key name to get its value.
    :param object default: a value to be returned if the provided
                           key is not present in request context.

    :returns: object
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_request_context(key, default)


def remove_request_context(key):
    """
    removes the specified key from current request context if available.

    :param str key: key name to be removed from request context.
    """

    get_component(SessionPackage.COMPONENT_NAME).remove_request_context(key)


def is_fresh():
    """
    gets a value indicating that current request has a fresh authentication.

    fresh authentication means an authentication which is done by providing
    user credentials to server.

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


def get_safe_component_custom_key():
    """
    gets component custom key in a safe manner.

    meaning that if the request does not exist in current context, it will
    return a None object instead of raising an error.

    :rtype: object
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_safe_component_custom_key()


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


def get_safe_cacheable_current_user():
    """
    gets cacheable current user in a safe manner.

    meaning that if the request does not exist in current context, it will
    return a None object instead of raising an error.
    """

    return get_component(SessionPackage.COMPONENT_NAME).get_safe_cacheable_current_user()


def is_request_context_available():
    """
    gets a value indicating that request context is available for usage.

    :rtype: bool
    """

    return get_component(SessionPackage.COMPONENT_NAME).is_request_context_available()
