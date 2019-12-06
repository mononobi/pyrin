# -*- coding: utf-8 -*-
"""
common models module.
"""

from sqlalchemy import Unicode, Integer

from pyrin.core.context import DTO
from pyrin.database.decorators import bind
from pyrin.database.model.base import CoreEntity
from pyrin.database.model.schema import CoreColumn


class SampleEntity(CoreEntity):
    """
    sample entity class.
    """

    __tablename__ = 'sample_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


@bind('local')
class BoundedLocalEntity(CoreEntity):
    """
    bounded local entity class.
    """

    __tablename__ = 'bounded_local_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


@bind('test')
class BoundedTestEntity(CoreEntity):
    """
    bounded test entity class.
    """

    __tablename__ = 'bounded_test_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


class SampleTestEntity(CoreEntity):
    """
    sample test entity class.
    """

    __tablename__ = 'sample_test_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


class SampleWithHiddenFieldBaseEntity(CoreEntity):
    """
    sample with hidden field base entity class.
    """

    __tablename__ = 'sample_with_hidden_field_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)


class SampleWithHiddenFieldEntity(SampleWithHiddenFieldBaseEntity):
    """
    sample with hidden field entity class.
    """

    __table_args__ = DTO(extend_existing=True)

    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)
    hidden_field = CoreColumn(name='hidden_field', type_=Unicode, hidden=True)
