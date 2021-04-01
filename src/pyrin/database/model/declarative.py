# -*- coding: utf-8 -*-
"""
model declarative module.

important note:

each `pyrin` package that references to this module, must
add `pyrin.database.model` into its `DEPENDS` list.
"""

from sqlalchemy.orm import DeclarativeMeta

import pyrin.database.model.services as model_services

from pyrin.database.model.base import BaseEntity


class CoreEntity(BaseEntity, metaclass=DeclarativeMeta):
    """
    core entity class.

    it should be used as the base class for all application concrete models.

    it is also possible to implement a new customized declarative base class for your
    application models. to do this you must subclass it from `BaseEntity`, because
    application will check isinstance() on `BaseEntity` type to detect models. then
    implement customized or new features in your subclassed `BaseEntity`. keep in mind
    that you should not subclass directly from `CoreEntity`, because it is a `DeclarativeMeta`
    and sqlalchemy raises an error if you subclass from this as your new declarative
    base class. note that your application must have a unique declarative base class for all
    models, do not mix the use of your new base class and `CoreEntity`, otherwise you will
    face problems in migrations and also multi-database environments.
    """

    __abstract__ = True
    registry = model_services.get_mapper_registry()
    metadata = model_services.get_mapper_registry().metadata
