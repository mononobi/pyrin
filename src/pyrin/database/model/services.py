# -*- coding: utf-8 -*-
"""
model services module.
"""

from pyrin.application.services import get_component
from pyrin.database.model import ModelPackage


def get_declarative_base():
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

    return get_component(ModelPackage.COMPONENT_NAME).get_declarative_base()


def get_metadata():
    """
    gets metadata of current declarative base.

    :rtype: MetaData
    """

    return get_component(ModelPackage.COMPONENT_NAME).get_metadata()


def get_tables():
    """
    gets all tables defined in metadata of current declarative base.

    :returns: dict(str name, Table table)
    :rtype: dict
    """

    return get_component(ModelPackage.COMPONENT_NAME).get_tables()


def collect_entities():
    """
    collects all entity classes of application.

    it returns the count of collected entities.

    :rtype: int
    """

    return get_component(ModelPackage.COMPONENT_NAME).collect_entities()


def get_entities():
    """
    gets a tuple of all application collected entities.

    :raises EntitiesAreNotCollectedError: entities are not collected error.

    :rtype: tuple[BaseEntity]
    """

    return get_component(ModelPackage.COMPONENT_NAME).get_entities()


def register_hook(instance):
    """
    registers the given instance into model hooks.

    :param ModelHookBase instance: model hook instance to be registered.

    :raises InvalidModelHookTypeError: invalid model hook type error.
    """

    return get_component(ModelPackage.COMPONENT_NAME).register_hook(instance)


def get_mapper_registry():
    """
    gets the configured mapper registry.

    :rtype: registry
    """

    return get_component(ModelPackage.COMPONENT_NAME).get_mapper_registry()
