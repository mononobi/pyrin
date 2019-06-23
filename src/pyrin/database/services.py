# -*- coding: utf-8 -*-
"""
database services module.
"""

from pyrin.application.services import get_component
from pyrin.database import DatabasePackage


def get_current_session():
    """
    gets current database session.

    :returns: database session
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_current_session()
