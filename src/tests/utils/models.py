# -*- coding: utf-8 -*-
"""
utils models module.
"""

from sqlalchemy import Column, Unicode, Integer

from pyrin.database.model.base import CoreEntity


class SampleEntity(CoreEntity):
    """
    sample entity class.
    """

    __tablename__ = 'fake_table'

    id = Column(name='id', type_=Integer, primary_key=True, autoincrement=False)
    name = Column(name='name', type_=Unicode)
    age = Column(name='age', type_=Integer)
