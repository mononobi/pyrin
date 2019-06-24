# -*- coding: utf-8 -*-
"""
database services module.
"""

from pyrin.application.services import get_component
from pyrin.database import DatabasePackage


def get_current_store():
    """
    gets current database store.

    :returns: database session
    :rtype: Session
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_current_store()


def get_session_factory():
    """
    gets database session factory.
    this method should not be used directly for data manipulation.
    use `get_current_store` method instead.

    :returns: database session factory
    :rtype: Session
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_session_factory()
