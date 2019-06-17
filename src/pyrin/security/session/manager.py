# -*- coding: utf-8 -*-
"""
session manager module.
"""

from flask import request

from pyrin.core.context import CoreObject
from pyrin.security.session.exceptions import InvalidRequestContextKeyNameError


class SessionManager(CoreObject):
    """
    session manager class.
    """

    def get_current_user(self):
        """
        gets current user.

        :rtype: dict
        """

        return self.get_current_request_context().get('user', None)

    def get_current_request(self):
        """
        gets current request object.

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
        adds the given key/value pair into request context.

        :param str key: key to be added.
        :param object value: value to be added.

        :raises InvalidRequestContextKeyNameError: invalid request context key name error.
        """

        if key is None or len(key.strip()) == 0:
            raise InvalidRequestContextKeyNameError('Request context key could not be None.')

        self.get_current_request_context()[key] = value
