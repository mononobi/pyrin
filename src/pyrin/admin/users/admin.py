# -*- coding: utf-8 -*-
"""
admin users admin module.
"""

import pyrin.admin.users.services as admin_user_services

from pyrin.admin.decorators import admin
from pyrin.admin.page.base import AdminPage
from pyrin.admin.users.models import AdminUserEntity


@admin()
class AdminUserAdmin(AdminPage):
    entity = AdminUserEntity
    register_name = 'admin-users'
    name = 'Admin User'
    create_service = admin_user_services.create
    update_service = admin_user_services.update
    extra_data_fields = dict(password=str, confirm_password=str)
    list_fields = (AdminUserEntity.id, AdminUserEntity.username, AdminUserEntity.fullname,
                   AdminUserEntity.is_active, AdminUserEntity.is_superuser,
                   AdminUserEntity.last_login_at, AdminUserEntity.gender,
                   AdminUserEntity.mobile, AdminUserEntity.email,
                   AdminUserEntity.created_at, AdminUserEntity.modified_at)
