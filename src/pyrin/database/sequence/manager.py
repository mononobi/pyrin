# -*- coding: utf-8 -*-
"""
sequence manager module.
"""

from sqlalchemy import Sequence

from pyrin.core.context import CoreObject
from pyrin.database.services import get_current_store


class SequenceManager(CoreObject):
    """
    sequence manager class.
    """

    def get_next_value(self, name):
        """
        gets the next value of given sequence.

        :param str name: sequence name to get its next value.

        :rtype: int
        """

        store = get_current_store()
        seq = Sequence(name)

        return store.execute(seq)
