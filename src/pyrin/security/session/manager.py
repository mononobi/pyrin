# -*- coding: utf-8 -*-
"""
session manager module.
"""

from flask import request
from flask.ctx import has_request_context

from pyrin.core.context import DTO, Manager
from pyrin.security.session.exceptions import InvalidRequestContextKeyNameError, \
    CouldNotOverwriteCurrentUserError, InvalidUserError, InvalidComponentCustomKeyError


class SessionManager(Manager):
    """
    session manager class.
    """

    def get_current_user(self):
        """
        gets current user.
        """

        return self.get_current_request().user

    def set_current_user(self, user):
        """
        sets current user.

        :param user: user object.

        :raises InvalidUserError: invalid user error.
        :raises CouldNotOverwriteCurrentUserError: could not overwrite current user error.
        """

        if user is None:
            raise InvalidUserError('Request user could not be None.')

        if self.get_current_user() is not None:
            raise CouldNotOverwriteCurrentUserError('User has been already set for '
                                                    'current request, it could not '
                                                    'be overwritten.')

        self.get_current_request().user = user

    def get_current_request(self):
        """
        gets current request object.

        :raises RuntimeError: runtime error.

        :rtype: CoreRequest
        """

        with request:
            return request

    def get_current_request_context(self):
        """
        gets current request context.

        :rtype: dict
        """

        return self.get_current_request().context

    def add_request_context(self, key, value):
        """
        adds the given key/value pair into current request context.

        :param str key: key to be added.
        :param object value: value to be added.

        :raises InvalidRequestContextKeyNameError: invalid request context key name error.
        """

        if key is None or len(key.strip()) == 0:
            raise InvalidRequestContextKeyNameError('Request context key could not be None.')

        self.get_current_request_context()[key] = value

    def is_fresh(self):
        """
        gets a value indicating that current request has a fresh token.
        fresh token means a token which created upon providing user credentials
        to server, not using a refresh token.

        :rtype: bool
        """

        return self.get_current_token_payload().get('is_fresh', False)

    def get_current_token_payload(self):
        """
        gets current request's token payload.

        :rtype: dict
        """

        return self.get_current_request_context().get('token_payload', DTO())

    def get_current_token_header(self):
        """
        gets current request's token header.

        :rtype: dict
        """

        return self.get_current_request_context().get('token_header', DTO())

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

    def get_safe_current_request(self):
        """
        gets current request object in a safe manner.
        meaning that if the request does not exist in current context, it will
        return a None object instead of raising an error.

        :rtype: CoreRequest
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

    def is_request_context_available(self):
        """
        gets a value indicating that request context is available for usage.

        :rtype: bool
        """

        return has_request_context()
