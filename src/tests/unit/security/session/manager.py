# -*- coding: utf-8 -*-
"""
session manager module.
"""

from pyrin.security.session.manager import SessionManager as BaseSessionManager

from tests.unit.application.structs import CoreRequestMock
from tests.unit.security.session import SessionPackage


class SessionManager(BaseSessionManager):
    """
    session manager class.
    """

    package_class = SessionPackage

    def __init__(self):
        """
        initializes an instance of SessionManager.
        """

        super().__init__()

        self.__current_request_mock = None

    def get_current_request(self):
        """
        gets current request object.

        :rtype: CoreRequestMock
        """

        return self.__current_request_mock

    def get_safe_current_request(self):
        """
        gets current request object in a safe manner.

        meaning that if the request does not exist in current context, it will
        return a None object instead of raising an error.

        :rtype: CoreRequestMock
        """

        return self.__current_request_mock

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

    def set_access_token(self, token):
        """
        sets the given access token in current request.

        :param str token: access token.
        """

        self.__current_request_mock.headers['Authorization'] = token

    def set_refresh_token(self, token):
        """
        sets the given refresh token in current request.

        :param str token: refresh token.
        """

        self.__current_request_mock.headers['Cookie'] = f'Refresh-Auth={token}'
