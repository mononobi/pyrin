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

    :rtype: type[CoreEntity]
    """

    return get_component(ModelPackage.COMPONENT_NAME).get_declarative_base()
