# -*- coding: utf-8 -*-
"""
logging masking structs module.
"""

from werkzeug.datastructures import Headers

import pyrin.logging.masking.services as masking_services
import pyrin.utils.headers as header_utils

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

    # the value to be used for masked keys.
    MASK = '*'

    def __init__(self, mapping=None, **kwargs):
        """
        initializes an instance of MaskedDict.

        :param dict | MaskedDict | Headers | iterable mapping: values to create a
                                                               dict form them.
        """

        masked_kwargs = {}
        if len(kwargs) > 0:
            masked_kwargs = self._mask_dict(kwargs)

        if isinstance(mapping, MaskedDict):
            super().__init__(self._unify(mapping, masked_kwargs))

        elif isinstance(mapping, (dict, Headers)):
            temp = {}
            for key, value in mapping.items():
                if masking_services.should_mask(key) is True:
                    temp[key] = self.MASK
                else:
                    temp[key] = self._mask(value)

            super().__init__(self._unify(temp, masked_kwargs))

        elif isinstance(mapping, LIST_TYPES):
            temp = []
            for key, value in mapping:
                if masking_services.should_mask(key) is True:
                    temp.append((key, self._mask(value)))
                else:
                    temp.append((key, value))

            super().__init__(temp, **masked_kwargs)

        else:
            super().__init__(masked_kwargs)

    def _unify(self, mapping, kwargs):
        """
        returns a unified dict from given mapping dict and keyword arguments dict.

        :param dict mapping: a mapping dict.
        :param dict kwargs: an extra dict to be unified with mapping.

        :rtype: dict
        """

        if len(kwargs) <= 0:
            return mapping

        data = dict(mapping)
        data.update(kwargs)
        return data

    def _mask(self, value):
        """
        masks all required keys of given object.

        if given object is not a dict or Headers or a collection of those
        objects, it returns the same input value.

        :param dict | Headers | list | tuple | set value: a dict or Headers or a
                                                          collection of those types.

        :rtype: dict | list[dict] | tuple[dict] | set[dict]
        """

        if isinstance(value, Headers):
            return self._mask_headers(value)
        elif isinstance(value, dict):
            return self._mask_dict(value)
        elif isinstance(value, LIST_TYPES):
            return self._mask_list(value)
        return value

    def _mask_dict(self, value):
        """
        masks all required keys of given dict.

        :param dict value: dict to mask its keys.

        :rtype: dict
        """

        return MaskedDict(value)

    def _mask_headers(self, value):
        """
        masks all required keys of given Headers object.

        :param Headers value: Headers to mask its keys.

        :rtype: dict
        """

        headers = header_utils.convert_headers(value)
        return self._mask_dict(headers.to_dict())

    def _mask_list(self, items):
        """
        masks all required keys of different items of given iterable.

        :param iterable items: items to mask their keys.

        :rtype: list | tuple | set
        """

        result_type = type(items)
        results = []
        for item in items:
            results.append(self._mask(item))

        return result_type(results)
