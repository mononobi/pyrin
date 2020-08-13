# -*- coding: utf-8 -*-
"""
sequence manager module.
"""

from abc import abstractmethod

from sqlalchemy import Sequence

import pyrin.database.services as database_services

from pyrin.core.structs import Manager, DTO
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.sequence import SequencePackage
from pyrin.database.services import get_current_store


class SequenceManager(Manager):
    """
    sequence manager class.
    """

    package_class = SequencePackage

    def __init__(self):
        """
        initializes an instance of SequenceManager.
        """

        super().__init__()

        # a dictionary containing dialect name to method map.
        # different dialects may not all support the standard sequence
        # generation, so we need to provide different methods on different
        # dialects. for example on `mssql` and `sqlite`
        # in the form of: {str dialect_name: callable method}
        self._dialect_to_method_map = self._map_dialect_to_method()

    def get_next_value(self, entity_class, sequence):
        """
        gets the next value of given sequence.

        :param BaseEntity entity_class: entity class which this
                                        sequence is defined in.

        :param Sequence sequence: sequence object to get its next value.

        :rtype: int
        """

        engine = database_services.get_entity_engine(entity_class)

        method = self._dialect_to_method_map.get(engine.name, )

    def _default_next_value(self, engine, sequence):
        """
        gets the next value of given sequence.

        :param Sequence sequence: sequence object to get its next value.

        :rtype: int
        """

        store = get_current_store()
        seq = Sequence(name)

        return store.execute(seq)

    def _mssql_next_value(self, sequence):
        """
        gets the next value of given sequence.
        this method will be used on sql-server backend.

        :param Sequence sequence: sequence object to get its next value.

        :rtype: int
        """

        store = get_current_store()

        return store.execute('select next value for {sequence}'.
                             format(sequence=name)).scalar()

    @abstractmethod
    def _sqlite_next_value(self, sequence):
        """
        sqlite does not support sequences.
        so this method raises an error.

        :param Sequence sequence: sequence object to get its next value.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError('sqlite database does not support sequences.')

    def _map_dialect_to_method(self):
        """
        maps different dialects to relevant methods.

        :returns: dict[str dialect_name: callable method]
        :rtype: dict
        """

        result = DTO(default=self._default_next_value,
                     mssql=self._mssql_next_value,
                     sqlite=self._sqlite_next_value)

        return result
