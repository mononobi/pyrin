# -*- coding: utf-8 -*-
"""
common models module.
"""

from sqlalchemy import Unicode, Integer

from pyrin.core.context import DTO
from pyrin.database.decorators import bind
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

    def primary_key(self):
        """
        gets the primary key value of this table.

        :rtype: str
        """

        return self.id


@bind('local')
class BoundedLocalEntity(CoreEntity):
    """
    bounded local entity class.
    """

    __tablename__ = 'bounded_local_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)

    def primary_key(self):
        """
        gets the primary key value of this table.

        :rtype: int
        """

        return self.id


@bind('test')
class BoundedTestEntity(CoreEntity):
    """
    bounded test entity class.
    """

    __tablename__ = 'bounded_test_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)

    def primary_key(self):
        """
        gets the primary key value of this table.

        :rtype: int
        """

        return self.id


@bind('local')
class ManualBoundedLocalEntity(CoreEntity):
    """
    manual bounded local entity class.
    """

    __tablename__ = 'manual_bounded_local_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)

    def primary_key(self):
        """
        gets the primary key value of this table.

        :rtype: int
        """

        return self.id


class SampleTestEntity(CoreEntity):
    """
    sample test entity class.
    """

    __tablename__ = 'sample_test_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = CoreColumn(name='name', type_=Unicode)
    age = CoreColumn(name='age', type_=Integer)

    def primary_key(self):
        """
        gets the primary key value of this table.

        :rtype: int
        """

        return self.id


class SampleWithHiddenFieldBaseEntity(CoreEntity):
    """
    sample with hidden field base entity class.
    """

    __tablename__ = 'sample_with_hidden_field_table'

    id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
    sub_id = CoreColumn(name='sub_id', type_=Unicode, primary_key=True)

    def primary_key(self):
        """
        gets the primary key value of this table.

        :returns tuple(int, str)
        :rtype: tuple
        """

        return self.id, self.sub_id


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

    def primary_key(self):
        """
        gets the primary key value of this table.

        :rtype: int
        """

        return self.id


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
