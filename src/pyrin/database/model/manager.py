# -*- coding: utf-8 -*-
"""
model manager module.
"""

import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.core.mixin import HookMixin
from pyrin.core.structs import Manager
from pyrin.database.model import ModelPackage
from pyrin.database.model.base import CoreEntity
from pyrin.database.model.hooks import ModelHookBase
from pyrin.database.model.exceptions import EntitiesAreNotCollectedError, \
    InvalidModelHookTypeError


class ModelManager(Manager, HookMixin):
    """
    model manager class.
    """

    hook_type = ModelHookBase
    invalid_hook_type_error = InvalidModelHookTypeError
    package_class = ModelPackage

    def __init__(self):
        """
        initializes an instance of ModelManager.
        """

        super().__init__()

        # a tuple containing all application entity classes.
        self._entities = None

    def _after_entities_collected(self):
        """
        this will call `after_entities_collected` method of registered hooks.
        """

        for hook in self._get_hooks():
            hook.after_entities_collected()

    def get_declarative_base(self):
        """
        gets the application's declarative base class.

        by default it returns `CoreEntity` class.
        if you want to define a new declarative base class in your application
        instead of using `CoreEntity` which is provided by pyrin, you must
        override this method inside your application's `database.model.ModelManager`
        class and return your new declarative base class.
        this is required if you want to enable migrations in your application.
        note that your application must have a unique declarative base type and
        you shouldn't mix the usage of `CoreEntity` and your new declarative base,
        otherwise migrations will not work properly.

        but, if you don't want to use migrations at all, you could just put
        `pyrin.database.migration` into `ignored_packages` list of `packaging.ini`
        file and leave this method unimplemented.

        :rtype: type[BaseEntity]
        """

        return CoreEntity

    def get_metadata(self):
        """
        gets metadata of current declarative base.

        :rtype: MetaData
        """

        return self.get_declarative_base().metadata

    def get_tables(self):
        """
        gets all tables defined in metadata of current declarative base.

        :returns: dict(str name, Table table)
        :rtype: dict
        """

        return self.get_metadata().tables

    def collect_entities(self):
        """
        collects all entity classes of application.

        it returns the count of collected entities.

        :rtype: int
        """

        base = self.get_declarative_base()
        result = []
        for table in self.get_tables().values():
            entity = sqlalchemy_utils.get_class_by_table(base, table, raise_multi=False)
            if entity is not None:
                result.append(entity)

        self._entities = tuple(result)
        self._after_entities_collected()
        return len(result)

    def get_entities(self):
        """
        gets a tuple of all application collected entities.

        :raises EntitiesAreNotCollectedError: entities are not collected error.

        :rtype: tuple[BaseEntity]
        """

        if self._entities is None:
            raise EntitiesAreNotCollectedError('Application entities are not collected yet.')

        return self._entities
