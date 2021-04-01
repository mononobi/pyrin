# -*- coding: utf-8 -*-
"""
caching models module.
"""

from sqlalchemy import LargeBinary

from pyrin.database.model.declarative import CoreEntity
from pyrin.database.model.mixin import CreateHistoryMixin
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.sql.schema.columns import AutoPKColumn, StringColumn, BigIntegerColumn


class CacheItemBaseEntity(CoreEntity):
    """
    cache item base entity class.
    """

    _table = 'cache_item'

    id = AutoPKColumn(name='id')


class CacheItemEntity(CacheItemBaseEntity, CreateHistoryMixin):
    """
    cache item entity class.
    """

    _extend_existing = True

    cache_name = StringColumn(name='cache_name', max_length=30, nullable=False)
    shard_name = StringColumn(name='shard_name', max_length=30, nullable=True)
    version = StringColumn(name='version', max_length=20, nullable=False)
    key = BigIntegerColumn(name='key', nullable=False)
    item = CoreColumn(name='item', type_=LargeBinary, nullable=False)
