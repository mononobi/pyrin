# -*- coding: utf-8 -*-
"""
common models module.
"""

from sqlalchemy import Column, Unicode, Integer

from pyrin.database.decorators import bind
from pyrin.database.model.base import CoreEntity


class SampleEntity(CoreEntity):
    """
    sample entity class.
    """

    __tablename__ = 'sample_table'

    id = Column(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = Column(name='name', type_=Unicode)
    age = Column(name='age', type_=Integer)


@bind('local')
class BoundedLocalEntity(CoreEntity):
    """
    bounded local entity class.
    """

    __tablename__ = 'bounded_local_table'

    id = Column(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = Column(name='name', type_=Unicode)
    age = Column(name='age', type_=Integer)


@bind('test')
class BoundedTestEntity(CoreEntity):
    """
    bounded test entity class.
    """

    __tablename__ = 'bounded_test_table'

    id = Column(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = Column(name='name', type_=Unicode)
    age = Column(name='age', type_=Integer)


class SampleTestEntity(CoreEntity):
    """
    sample test entity class.
    """

    __tablename__ = 'sample_test_table'

    id = Column(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = Column(name='name', type_=Unicode)
    age = Column(name='age', type_=Integer)
