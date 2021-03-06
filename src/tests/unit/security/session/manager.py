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
