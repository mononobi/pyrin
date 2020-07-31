# -*- coding: utf-8 -*-
"""
logging masking structs module.
"""

import pyrin.logging.masking.services as masking_services

from pyrin.core.globals import LIST_TYPES
from pyrin.core.structs import CoreImmutableDict


class MaskedDict(CoreImmutableDict):
    """
    masked dict class.

    this class is a normal dict with the ability of masking
    values of specific keys in the dict.
    note that this type is immutable. meaning that values or keys of
    dict could not be changed after initialization.
    """

    def __init__(self, mapping=None, **kwargs):
        """
        initializes an instance of MaskedDict.

        :param dict | MaskedDict mapping: values to create a dict form them.
        """

        masked_kwargs = {}
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if masking_services.should_mask(key) is True:
                    masked_kwargs[key] = '*'
                else:
                    if isinstance(value, dict):
                        value = self._mask_dict(value)
                    elif isinstance(value, LIST_TYPES):
                        value = self._mask_list(value)
                    masked_kwargs[key] = value

        if isinstance(mapping, MaskedDict):
            super().__init__(mapping, **masked_kwargs)

        elif isinstance(mapping, dict):
            temp = {}
            for key, value in mapping.items():
                if masking_services.should_mask(key) is True:
                    temp[key] = '*'
                else:
                    if isinstance(value, dict):
                        value = self._mask_dict(value)
                    elif isinstance(value, LIST_TYPES):
                        value = self._mask_list(value)
                    temp[key] = value
            super().__init__(temp, **masked_kwargs)

        else:
            super().__init__(**masked_kwargs)

    def _mask_dict(self, value):
        """
        masks all required keys of given dict.

        :param dict value: dict to mask its keys.

        :rtype: dict
        """

        return MaskedDict(value)

    def _mask_list(self, items):
        """
        masks all required keys of different items of given iterable.

        :param list | tuple | set items: items to mask their keys.

        :rtype lis | tuple | set
        """

        result_type = type(items)
        results = []
        for item in items:
            if isinstance(item, dict):
                results.append(self._mask_dict(item))
            elif isinstance(item, LIST_TYPES):
                results.append(self._mask_list(item))
            else:
                results.append(item)

        return result_type(results)
