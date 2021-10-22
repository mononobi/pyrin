# -*- coding: utf-8 -*-
"""
caching admin module.
"""

from pyrin.admin.decorators import admin
from pyrin.admin.page.base import AdminPage
from pyrin.caching.models import CacheItemEntity


@admin()
class CacheItemAdmin(AdminPage):
    entity = CacheItemEntity
    register_name = 'cache-items'
    name = 'Cache Item'
    create_permission = False
    update_permission = False
    list_fields = (CacheItemEntity.id, CacheItemEntity.cache_name,
                   CacheItemEntity.shard_name, CacheItemEntity.version,
                   CacheItemEntity.key, CacheItemEntity.created_at)
