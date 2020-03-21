# -*- coding: utf-8 -*-
"""
sequence component module.
"""

from pyrin.application.decorators import component
from pyrin.database.sequence import SequencePackage
from pyrin.database.sequence.manager import SequenceManager
from pyrin.application.structs import Component


@component(SequencePackage.COMPONENT_NAME)
class SequenceComponent(Component, SequenceManager):
    """
    sequence component class.
    """
    pass
