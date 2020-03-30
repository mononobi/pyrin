# -*- coding: utf-8 -*-
"""
sequence test_services module.
"""

import pytest

from sqlalchemy.schema import CreateSequence, DropSequence
from sqlalchemy import Sequence

import pyrin.database.sequence.services as sequence_services
import pyrin.database.services as database_services

from pyrin.database.services import get_current_store


@pytest.mark.skipif('database_services.get_default_engine().name in ("sqlite", "mssql")',
                    'sqlite database does not support sequences, so this test has skipped.'
                    'sqlalchemy currently does not support sql server sequence creation, '
                    'so this test has skipped.')
def test_get_next_value():
    """
    gets the next value of given sequence.
    note that sqlite database does not support sequences.
    so we do not test it on sqlite.
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
