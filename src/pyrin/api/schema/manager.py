# -*- coding: utf-8 -*-
"""
schema manager module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.api.schema import SchemaPackage
from pyrin.core.structs import Manager


class SchemaManager(Manager):
    """
    schema manager class.
    """

    package_class = SchemaPackage

    def get_computed_entity_columns(self, entity, result_schema=None, **options):
        """
        gets a dict containing all computed columns to be added to the result.

        if `result_schema` is not provided, it returns an empty dict.
        note that the result dict should not contain any `BaseEntity` or
        `ROW_RESULT` values, otherwise a max recursion error may occur.

        :param BaseEntity entity: the actual entity to be processed.
        :param ResultSchema result_schema: result schema to be used for computation.

        :rtype: dict
        """

        if result_schema is None:
            return {}

        result = result_schema.get_computed_entity_columns(entity, **options)
        if result is None:
            return {}

        options.update(result_schema=result_schema)
        result = serializer_services.serialize(result, **options)
        return result

    def get_computed_row_columns(self, row, result_schema=None, **options):
        """
        gets a dict containing all computed columns to be added to the result.

        if `result_schema` is not provided, it returns an empty dict.
        note that the result dict should not contain any `BaseEntity` or
        `ROW_RESULT` values, otherwise a max recursion error may occur.

        :param ROW_RESULT row: the actual row result to be processed.
        :param ResultSchema result_schema: result schema to be used for computation.

        :rtype: dict
        """

        if result_schema is None:
            return {}

        result = result_schema.get_computed_row_columns(row, **options)
        if result is None:
            return {}

        options.update(result_schema=result_schema)
        result = serializer_services.serialize(result, **options)
        return result
