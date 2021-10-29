# -*- coding: utf-8 -*-
"""
authentication test authenticators package.
"""

from pyrin.security.authentication.decorators import authenticator
from pyrin.security.authentication.handlers.base import TokenAuthenticatorBase


@authenticator()
class TestAccessTokenAuthenticator(TokenAuthenticatorBase):
    """
    test access token authenticator.
    """

    _name = 'test'

    def _get_user_identity(self, user, **options):
        """
        gets the identity of given user to be set in current request.

        the identity is normally the primary key of user entity.
        but it could be a dict of multiple values if required.

        :param BaseEntity | ROW_RESULT user: user entity to get its identity.

        :rtype: object | dict
        """

        return user.get('id')

    def _get_user(self, payload, **options):
        """
        gets the user entity from given inputs.

        this method must return a user on success or raise an error
        if it can not fetch related user to given payload.

        :param dict | str payload: credential payload.

        :rtype: BaseEntity | ROW_RESULT
        """

        return dict(id=payload.get('sub'))
