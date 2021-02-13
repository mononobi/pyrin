# -*- coding: utf-8 -*-
"""
caching models module.
"""

from sqlalchemy import BigInteger, Unicode, LargeBinary

from pyrin.database.model.base import CoreEntity
from pyrin.database.model.mixin import HistoryMixin
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.sql.schema.columns import AutoPKColumn


class CacheItemBaseEntity(CoreEntity):
    """
    cache item base entity class.
    """

    _table = 'cache_item'

    id = AutoPKColumn(name='id')


class CacheItemEntity(CacheItemBaseEntity, HistoryMixin):
    """
    cache item entity class.
    """

    _extend_existing = True

    cache_name = CoreColumn(name='cache_name', type_=Unicode(length=25), nullable=False)
    shard_name = CoreColumn(name='shard_name', type_=Unicode(25), nullable=True)
    version = CoreColumn(name='version', type_=Unicode(length=20), nullable=False)
    key = CoreColumn(name='key', type_=BigInteger, nullable=False)
    item = CoreColumn(name='item', type_=LargeBinary, nullable=False)
