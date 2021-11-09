# -*- coding: utf-8 -*-
"""
users internal admin module.
"""

import pyrin.users.internal.services as internal_user_services

from pyrin.admin.decorators import admin
from pyrin.admin.page.base import AdminPage
from pyrin.admin.page.decorators import link
from pyrin.users.internal.models import InternalUserEntity
from pyrin.security.authentication.models import InternalSessionEntity


@admin()
class InternalUserAdmin(AdminPage):
    entity = InternalUserEntity
    register_name = 'internal-users'
    name = 'Internal User'
    category = 'USERS'
    create_service = internal_user_services.create
    update_service = internal_user_services.update
    extra_data_fields = dict(password=str, confirm_password=str)
    list_search_fields = (InternalUserEntity.email,)
    list_fields = (InternalUserEntity.id, InternalUserEntity.username,
                   InternalUserEntity.fullname, InternalUserEntity.is_active,
                   InternalUserEntity.is_superuser, InternalUserEntity.admin_access,
                   InternalUserEntity.audit_access, InternalUserEntity.swagger_access,
                   InternalUserEntity.mobile, InternalUserEntity.gender,
                   InternalUserEntity.last_login_at, InternalUserEntity.created_at,
                   InternalUserEntity.modified_at, 'sessions')

    @link
    def sessions(self, row):
        """
        gets all related sessions to this user.

        :param ROW_RESULT row: user row.

        :rtype: dict
        """

        return self._get_link_info('Sessions', InternalSessionEntity, user_id=row.id)


@admin()
class InternalSessionAdmin(AdminPage):
    entity = InternalSessionEntity
    register_name = 'internal-sessions'
    name = 'Internal Session'
    category = 'AUTHENTICATION'
    list_fields = (InternalSessionEntity.id, InternalSessionEntity.user_id,
                   InternalUserEntity.fullname, InternalSessionEntity.type,
                   InternalSessionEntity.authenticator, InternalSessionEntity.is_revoked,
                   InternalSessionEntity.created_at, InternalSessionEntity.modified_at)

    def _perform_joins(self, query, **options):
        query = query.join(InternalUserEntity,
                           InternalSessionEntity.user_id == InternalUserEntity.id)
        return query
