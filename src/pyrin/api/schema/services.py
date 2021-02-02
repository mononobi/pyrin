# -*- coding: utf-8 -*-
"""
schema services module.
"""

from pyrin.application.services import get_component
from pyrin.api.schema import SchemaPackage


def get_computed_entity_columns(entity, result_schema=None, **options):
    """
    gets a dict containing all computed columns to be added to the result.

    if `result_schema` is not provided, it returns an empty dict.
    note that the result dict should not contain any `BaseEntity` or
    `ROW_RESULT` values, otherwise a max recursion error may occur.

    :param BaseEntity entity: the actual entity to be processed.
    :param ResultSchema result_schema: result schema to be used for computation.

    :rtype: dict
    """

    return get_component(SchemaPackage.COMPONENT_NAME).get_computed_entity_columns(entity,
                                                                                   result_schema,
                                                                                   **options)


def get_computed_row_columns(row, result_schema=None, **options):
    """
    gets a dict containing all computed columns to be added to the result.

    if `result_schema` is not provided, it returns an empty dict.
    note that the result dict should not contain any `BaseEntity` or
    `ROW_RESULT` values, otherwise a max recursion error may occur.

    :param ROW_RESULT row: the actual row result to be processed.
    :param ResultSchema result_schema: result schema to be used for computation.

    :rtype: dict
    """

    return get_component(SchemaPackage.COMPONENT_NAME).get_computed_row_columns(row,
                                                                                result_schema,
                                                                                **options)
