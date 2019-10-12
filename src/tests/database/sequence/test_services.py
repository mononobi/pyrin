# -*- coding: utf-8 -*-
"""
sequence test_services module.
"""

from sqlalchemy.schema import CreateSequence, DropSequence
from sqlalchemy import Sequence

import pyrin.database.sequence.services as sequence_services

from pyrin.database.services import get_current_store


def test_get_next_value():
    """
    gets the next value of given sequence.
    """

    store = get_current_store()
    name = 'test_get_next_value_seq'
    sequence = Sequence(name, start=1, increment=1, minvalue=1)
    create_statement = CreateSequence(sequence)
    store.execute(create_statement)
    try:
        first_value = sequence_services.get_next_value(name)
        second_value = sequence_services.get_next_value(name)
        third_value = sequence_services.get_next_value(name)

        assert first_value == 1 and second_value == 2 and third_value == 3
    finally:
        drop_statement = DropSequence(sequence)
        store.execute(drop_statement)
