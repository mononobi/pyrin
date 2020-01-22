# -*- coding: utf-8 -*-
"""
database migration adapters module.
"""

from copy import deepcopy

from sqlalchemy import MetaData

from pyrin.core.context import CoreObject


class MetaDataAdapter(CoreObject):
    """
    metadata adapter class.
    this class would only be used for migration management.
    it provides facilities for the operations that alembic
    will do on `MetaData` by providing a common api with `MetaData`.
    """

    def __init__(self, metadata, tables):
        """
        initializes an instance of MetaDataAdapter.

        :param MetaData metadata: metadata object to be adapted.
        :param list[Tables] tables: tables that this metadata should represent.
        """

        CoreObject.__init__(self)
        self.metadata = deepcopy(metadata)
        self.process_tables(self.metadata, tables)
        self.schema = self.metadata.schema
        self.naming_convention = self.metadata.naming_convention
        self.info = self.metadata.info
        self.bind = self.metadata.bind
        self.tables = self.metadata.tables

    def process_tables(self, metadata, tables):
        """
        processes the tables that this metadata must represent.

        :param MetaData metadata: metadata object to get available tables from it.
        :param list[Tables] tables: tables that this metadata should represent.
        """

        requested_tables_fullname = [table.fullname for table in tables]
        all_tables = [table for table in metadata.tables.values()]
        for table in all_tables:
            if table.fullname not in requested_tables_fullname:
                self.metadata.remove(table)

    @property
    def sorted_tables(self):
        """
        returns a list of `Table` objects sorted in order of
        foreign key dependency.

        :returns: list[Table]
        :rtype: list
        """

        return self.metadata.sorted_tables
