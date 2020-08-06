# -*- coding: utf-8 -*-
"""
model cache module.
"""

from pyrin.caching.structs import SharedContainer


class ColumnCache(SharedContainer):
    """
    column cache class.

    this class is used to save column names (other than pk and fk) of different entity types.
    """

    _storage = dict()


class RelationshipCache(SharedContainer):
    """
    relationship cache class.

    this class is used to save relationship property names of different entity types.
    """

    _storage = dict()


class PropertyCache(SharedContainer):
    """
    property cache class.

    this class is used to save all property names of different entity types.
    """

    _storage = dict()


class PrimaryKeyCache(SharedContainer):
    """
    primary key cache class.

    this class is used to save primary key names of different entity types.
    """

    _storage = dict()


class ForeignKeyCache(SharedContainer):
    """
    foreign key cache class.

    this class is used to save foreign key names of different entity types.
    """

    _storage = dict()
