# -*- coding: utf-8 -*-
"""
model cache module.
"""

from pyrin.caching.structs import SharedContainer


class ModelLocalCache(SharedContainer):
    """
    model local cache class.

    all model cache classes must be subclassed from this.
    """

    _storage = dict()


class ColumnCache(ModelLocalCache):
    """
    column cache class.

    this class is used to save column names (other than pk and fk) of different entity types.
    """

    _storage = dict()


class RelationshipCache(ModelLocalCache):
    """
    relationship cache class.

    this class is used to save relationship property names of different entity types.
    """

    _storage = dict()


class HybridPropertyCache(ModelLocalCache):
    """
    hybrid property cache class.

    this class is used to save all hybrid property names of different entity types.
    """

    _storage = dict()


class AttributeCache(ModelLocalCache):
    """
    attribute cache class.

    this class is used to save all attribute names of different entity types.
    """

    _storage = dict()


class PrimaryKeyCache(ModelLocalCache):
    """
    primary key cache class.

    this class is used to save primary key names of different entity types.
    """

    _storage = dict()


class ForeignKeyCache(ModelLocalCache):
    """
    foreign key cache class.

    this class is used to save foreign key names of different entity types.
    """

    _storage = dict()


class MetadataCache(ModelLocalCache):
    """
    metadata cache class.

    this class is used to save metadata info for different entity types.
    """

    _storage = dict()
