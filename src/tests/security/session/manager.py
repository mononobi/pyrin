# -*- coding: utf-8 -*-
"""
session manager module.
"""

from pyrin.core.context import DTO
from pyrin.security.session.manager import SessionManager
from pyrin.security.session.exceptions import InvalidRequestContextKeyNameError, \
    InvalidComponentCustomKeyError

from tests.application.context import CoreRequestMock


class TestSessionManager(SessionManager):
    """
    test session manager class.
    """

    def __init__(self):
        """
        initializes an instance of TestSessionManager.
        """

        SessionManager.__init__(self)

        self.__current_request_mock = None

    def get_current_user(self):
        """
        gets current user object.

        :rtype: dict
        """

        return self.get_current_request().user

    def set_current_user(self, user):
        """
        sets current user object.

        :param dict user: user object.
        """

        self.get_current_request().user = user

    def get_current_request(self):
        """
        gets current request object.

        :rtype: CoreRequestMock
        """

        return self.__current_request_mock

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
        sets the component custom key in request.

        :param object value: component custom key value.

        :raises InvalidComponentCustomKeyError: invalid component custom key error.
        """

        if value is None:
            raise InvalidComponentCustomKeyError('Component custom key could not be None.')

        self.get_current_request().component_custom_key = value

    def get_component_custom_key(self):
        """
        gets component custom key from request.

        :rtype: object
        """

        return self.get_current_request().component_custom_key

    def inject_new_request(self):
        """
        injects a new request into current request object.
        """

        self.__current_request_mock = CoreRequestMock()

    def clear_current_request(self):
        """
        clears current request object.
        """

        self.__current_request_mock = None
