# -*- coding: utf-8 -*-
"""
common models module.
"""

from sqlalchemy import Unicode, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pyrin.core.structs import DTO
from pyrin.database.model.decorators import bind
from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.types.custom import GUID


class SampleEntity(CoreEntity):
    """
    sample entity class.
    """

    table = 'sample_table'

    id = CoreColumn(name='id', type_=GUID, primary_key=True)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


@bind('local')
class BoundedLocalEntity(CoreEntity):
    """
    bounded local entity class.
    """

    table = 'bounded_local_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


@bind('test')
class BoundedTestEntity(CoreEntity):
    """
    bounded test entity class.
    """

    table = 'bounded_test_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


@bind('local')
class ManualBoundedLocalEntity(CoreEntity):
    """
    manual bounded local entity class.
    """

    table = 'manual_bounded_local_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)


class SampleTestEntity(CoreEntity):
    """
    sample test entity class.
    """

    table = 'sample_test_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)
    sample_entity_id = CoreColumn(ForeignKey('sample_table.id'),
                                  name='sample_table_id', type_=GUID, index=True)


class SampleWithHiddenFieldBaseEntity(CoreEntity):
    """
    sample with hidden field base entity class.
    """

    table = 'sample_with_hidden_field_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    sub_id = CoreColumn(name='sub_id', type_=Unicode, primary_key=True)


class SampleWithHiddenFieldEntity(SampleWithHiddenFieldBaseEntity):
    """
    sample with hidden field entity class.
    """

    extend_existing = True

    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)
    hidden_field = CoreColumn(name='hidden_field', type_=Unicode, exposed=False)


class BaseEntity(CoreEntity):
    """
    base entity class.
    """

    table = 'base_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)


class SubBaseEntity(BaseEntity):
    """
    sub base entity class.
    """

    extend_existing = True

    age = CoreColumn(name='age', type_=Integer)


class RightChildEntity(SubBaseEntity):
    """
    right child entity class.
    """

    extend_existing = True

    grade = CoreColumn(name='grade', type_=Integer)


class LeftChildEntity(SubBaseEntity):
    """
    left child entity class.
    """

    extend_existing = True

    point = CoreColumn(name='point', type_=Integer)


class ParentEntity(CoreEntity):
    """
    parent entity class.
    """

    table = 'parent_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    children = relationship('ChildEntity', back_populates='parent', uselist=True)


class ChildEntity(CoreEntity):
    """
    child entity class.
    """

    table = 'child_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    parent_id = CoreColumn(ForeignKey('parent_table.id'),
                           name='parent_id', type_=Integer, index=True)
    parent = relationship('ParentEntity', back_populates='children', uselist=False)
