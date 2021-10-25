# -*- coding: utf-8 -*-
"""
users internal admin module.
"""

import pyrin.users.internal.services as internal_user_services

from pyrin.admin.decorators import admin
from pyrin.admin.page.base import AdminPage
from pyrin.users.internal.models import InternalUserEntity


@admin()
class InternalUserAdmin(AdminPage):
    entity = InternalUserEntity
    register_name = 'internal-users'
    name = 'Internal User'
    category = 'USERS'
    create_service = internal_user_services.create
    update_service = internal_user_services.update
    extra_data_fields = dict(password=str, confirm_password=str)
    list_fields = (InternalUserEntity.id, InternalUserEntity.username,
                   InternalUserEntity.fullname, InternalUserEntity.is_active,
                   InternalUserEntity.is_superuser, InternalUserEntity.admin_access,
                   InternalUserEntity.audit_access, InternalUserEntity.swagger_access,
                   InternalUserEntity.mobile, InternalUserEntity.email,
                   InternalUserEntity.gender, InternalUserEntity.last_login_at,
                   InternalUserEntity.created_at, InternalUserEntity.modified_at)
