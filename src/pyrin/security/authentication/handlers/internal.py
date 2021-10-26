# -*- coding: utf-8 -*-
"""
authentication handlers internal module.
"""

import pyrin.users.internal.services as internal_user_services

from pyrin.users.internal.models import InternalUserEntity
from pyrin.security.authentication.handlers.base import TokenAuthenticatorBase


class InternalTokenAuthenticator(TokenAuthenticatorBase):
    """
    internal token authenticator class.

    all application internal token authenticators must be subclassed from this.
    for example admin, swagger or audit authenticators.
    """

    def _get_user_info(self, user, **options):
        """
        gets the info of given user to be set in current request.

        it could be None if no extra info must be set in current request.

        :param ROW_RESULT user: internal user entity to get its info.

        :rtype: dict
        """

        result = dict(fullname=user.fullname,
                      is_active=user.is_active,
                      is_superuser=user.is_superuser)

        extra_info = self._get_extra_user_info(user, **options)
        if extra_info:
            result.update(extra_info)

        return result

    def _get_user_identity(self, user, **options):
        """
        gets the identity of given user to be set in current request.

        the identity is normally the primary key of user entity.
        but it could be a dict of multiple values if required.

        :param ROW_RESULT user: internal user entity to get its identity.

        :rtype: int
        """

        return user.id

    def _get_user(self, payload, **options):
        """
        gets the internal user from given access token payload.

        this method must return an internal user on success or raise an
        exception if it can not fetch related user to given access token payload.

        :param dict payload: access token payload.

        :rtype: ROW_RESULT
        """

        user_id = payload.get(self.USER_IDENTITY_HOLDER)
        return internal_user_services.get(user_id,
                                          InternalUserEntity.id,
                                          InternalUserEntity.is_active,
                                          InternalUserEntity.is_superuser,
                                          InternalUserEntity.swagger_access,
                                          InternalUserEntity.audit_access,
                                          InternalUserEntity.admin_access,
                                          InternalUserEntity.fullname)

    def _get_extra_user_info(self, user, **options):
        """
        gets extra user info for given internal user if required.

        this method is intended to be overridden in subclasses.

        :param ROW_RESULT user: internal user to get its extra info.

        :rtype: dict
        """

        return None
