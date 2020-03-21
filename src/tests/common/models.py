# -*- coding: utf-8 -*-
"""
common models module.
"""

from sqlalchemy import Unicode, Integer, ForeignKey

from pyrin.core.structs import DTO
from pyrin.database.model.decorators import bind
from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.types.custom import GUID


class SampleEntity(CoreEntity):
    """
    sample entity class.
    """

    __tablename__ = 'sample_table'

    id = CoreColumn(name='id', type_=GUID, primary_key=True)
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


@bind('local')
class ManualBoundedLocalEntity(CoreEntity):
    """
    manual bounded local entity class.
    """

    __tablename__ = 'manual_bounded_local_table'

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
    sample_entity_id = CoreColumn(ForeignKey('sample_table.id'),
                                  name='sample_table_id', type_=GUID, index=True)


class SampleWithHiddenFieldBaseEntity(CoreEntity):
    """
    sample with hidden field base entity class.
    """

    __tablename__ = 'sample_with_hidden_field_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    sub_id = CoreColumn(name='sub_id', type_=Unicode, primary_key=True)


class SampleWithHiddenFieldEntity(SampleWithHiddenFieldBaseEntity):
    """
    sample with hidden field entity class.
    """

    __table_args__ = DTO(extend_existing=True)

    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)
    hidden_field = CoreColumn(name='hidden_field', type_=Unicode, exposed=False)


class BaseEntity(CoreEntity):
    """
    base entity class.
    """

    __tablename__ = 'base_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)


class SubBaseEntity(BaseEntity):
    """
    sub base entity class.
    """

    __table_args__ = DTO(extend_existing=True)

    age = CoreColumn(name='age', type_=Integer)


class RightChildEntity(SubBaseEntity):
    """
    right child entity class.
    """

    __table_args__ = DTO(extend_existing=True)

    grade = CoreColumn(name='grade', type_=Integer)


class LeftChildEntity(SubBaseEntity):
    """
    left child entity class.
    """

    __table_args__ = DTO(extend_existing=True)

    point = CoreColumn(name='point', type_=Integer)
