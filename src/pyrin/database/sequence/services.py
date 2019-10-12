# -*- coding: utf-8 -*-
"""
sequence services module.
"""

from pyrin.application.services import get_component
from pyrin.database.sequence import SequencePackage


def get_next_value(name):
    """
    gets the next value of given sequence.

    :param str name: sequence name to get its next value.

    :rtype: int
    """

    return get_component(SequencePackage.COMPONENT_NAME).get_next_value(name)
