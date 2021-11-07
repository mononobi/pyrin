# -*- coding: utf-8 -*-
"""
session manager module.
"""

from flask import request
from flask.ctx import has_request_context

import pyrin.security.authentication.services as authentication_services
import pyrin.security.authorization.services as authorization_services

from pyrin.core.structs import Manager
from pyrin.security.session import SessionPackage
from pyrin.security.session.exceptions import InvalidUserError, \
    CouldNotOverwriteCurrentUserError, InvalidComponentCustomKeyError


class SessionManager(Manager):
    """
    session manager class.
    """

    package_class = SessionPackage

    def get_current_user(self):
        """
        gets current user identity.

        :returns: object
        """

        return self.get_current_request().user

    def get_current_user_info(self):
        """
        gets current user info.

        it may return None if user info is not set.

        :rtype: dict
        """

        return self.get_current_request().user_info

    def set_current_user(self, user, info=None):
        """
        sets current user.

        :param user: user identity object.
        :param dict info: user info.

        :raises InvalidUserError: invalid user error.
        :raises CouldNotOverwriteCurrentUserError: could not overwrite current user error.
        """

        if user is None:
            raise InvalidUserError('Request user could not be None.')

        current_request = self.get_current_request()
        if current_request.user is not None:
            raise CouldNotOverwriteCurrentUserError('User has been already set for '
                                                    'current request, it could not '
                                                    'be overwritten.')

        current_request.user = user
        current_request.user_info = info

    def get_current_request(self):
        """
        gets current request object.

        :raises RuntimeError: runtime error.

        :rtype: pyrin.processor.request.wrappers.base.CoreRequest
        """

        return request

    def get_current_request_id(self):
        """
        gets current request id.

        this method is implemented to overcome the hash problem of requests.
        `CoreRequest` objects are hashable themselves, but when they used as a dict key
        some hash collisions will occur. so we have to expose the exact request id to
        be able to use it as a dict key in places such as database scoped sessions.

        :raises RuntimeError: runtime error.

        :rtype: uuid.UUID
        """

        return self.get_current_request().request_id

    def add_request_context(self, key, value, **options):
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

        self.get_current_request().add_context(key, value, **options)

    def get_request_context(self, key, default=None):
        """
        gets the value for given key from current request context.

        it gets the default value if key is not present in the request context.

        :param str key: key name to get its value.
        :param object default: a value to be returned if the provided
                               key is not present in request context.

        :returns: object
        """

        return self.get_current_request().get_context(key, default)

    def remove_request_context(self, key):
        """
        removes the specified key from current request context if available.

        :param str key: key name to be removed from request context.
        """

        self.get_current_request().remove_context(key)

    def is_fresh(self):
        """
        gets a value indicating that current request has a fresh authentication.

        fresh authentication means an authentication which is done by providing
        user credentials to server.

        :rtype: bool
        """

        authenticator = authentication_services.get_current_authenticator()
        if authenticator is not None:
            return authenticator.is_fresh()

        return False

    def set_component_custom_key(self, value):
        """
        sets the component custom key.

        :param object value: component custom key value.

        :raises InvalidComponentCustomKeyError: invalid component custom key error.
        """

        if value is None:
            raise InvalidComponentCustomKeyError('Component custom key could not be None.')

        self.get_current_request().component_custom_key = value

    def get_component_custom_key(self):
        """
        gets component custom key.

        :rtype: object
        """

        return self.get_current_request().component_custom_key

    def get_safe_component_custom_key(self):
        """
        gets component custom key in a safe manner.

        meaning that if the request does not exist in current context, it will
        return a None object instead of raising an error.

        :rtype: object
        """

        current_request = self.get_safe_current_request()
        if current_request is None:
            return None

        return current_request.component_custom_key

    def get_safe_current_request(self):
        """
        gets current request object in a safe manner.

        meaning that if the request does not exist in current context, it will
        return a None object instead of raising an error.

        :rtype: pyrin.processor.request.wrappers.base.CoreRequest
        """

        if self.is_request_context_available() is True:
            return self.get_current_request()

        return None

    def get_safe_current_user(self):
        """
        gets current user in a safe manner.

        meaning that if the request does not exist in current context, it will
        return a None object instead of raising an error.
        """

        current_request = self.get_safe_current_request()
        if current_request is None:
            return None

        return current_request.user

    def get_safe_cacheable_current_user(self):
        """
        gets cacheable current user in a safe manner.

        meaning that if the request does not exist in current context, it will
        return a None object instead of raising an error.
        """

        current_request = self.get_safe_current_request()
        if current_request is None:
            return None

        return current_request.cacheable_user

    def is_request_context_available(self):
        """
        gets a value indicating that request context is available for usage.

        :rtype: bool
        """

        return has_request_context()

    def is_superuser(self):
        """
        gets a value indicating that the current user is superuser.

        :rtype: bool
        """

        authorizer_name = authentication_services.get_current_authenticator_name()
        if authorizer_name is None or \
                not authorization_services.authorizer_exists(authorizer_name):
            return False

        authorizer = authorization_services.get_authorizer(authorizer_name)
        return authorizer.is_superuser()

    def set_response_cookie(self, key, value, path='/',
                            secure=False, httponly=False, **options):
        """
        sets a response cookie that client should send on subsequent requests.

        :param str key: the key (name) of the cookie to be set.
        :param str value: the value of the cookie.

        :param str path: limits the cookie to a given path, per default
                         it will span the whole domain.

        :param bool secure: if `True`, the cookie will only be available via HTTPS.
        :param bool httponly: disallow JavaScript access to the cookie.

        :keyword timedelta | int max_age: should be a number of seconds, or `None`
                                          (default) if the cookie should last only
                                          as long as the client's browser session.

        :keyword str | datetime | int | float expires: should be a `datetime`
                                                       object or UNIX timestamp.

        :keyword str domain: if you want to set a cross-domain cookie.
                             for example, `domain=".example.com"` will set a
                             cookie that is readable by the domain `www.example.com`,
                             `foo.example.com`` etc. otherwise, a cookie will only
                             be readable by the domain that set it.

        :keyword samesite: limit the scope of the cookie to only be
                           attached to requests that are `same-site`.

        :enum samesite:
            STRICT = 'Strict'
            LAX = 'Lax'
            NONE = 'None'
        """

        current_request = self.get_current_request()
        current_request.set_response_cookie(key, value, path,
                                            secure, httponly, **options)
