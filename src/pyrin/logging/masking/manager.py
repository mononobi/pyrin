# -*- coding: utf-8 -*-
"""
logging masking manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.core.structs import Manager
from pyrin.logging.masking.structs import MaskedDict


class LoggingMaskingManager(Manager):
    """
    logging masking manager class.
    """

    # theses are default keywords that will be masked if they are present in a dict.
    # these values could be extended or disabled in 'logging.masking' config store.
    DEFAULT_MASKED_KEYWORDS = {'password', 'passwd', 'pass', 'email', 'email_address',
                               'token', 'auth_token', 'authtoken', 'api_key', 'apikey',
                               'secret_key', 'secret', 'credit_card', 'credit_card_no',
                               'credit_card_number', 'card_number', 'card_no', 'phone',
                               'phone_number', 'phone_no', 'mobile', 'mobile_no',
                               'mobile_number', 'address', 'postal_address', 'postal_code',
                               'zip_code', 'national_code', 'national_no', 'national_number',
                               'identity_code', 'identity_no', 'identity_number', 'birth_date',
                               'birthdate', 'authentication', 'authorization', 'home_address',
                               'birth_certificate', 'birth_certificate_no', 'passport_number',
                               'birth_certificate_number', 'passport', 'passport_no'}

    def __init__(self):
        """
        initializes an instance of LoggingMaskingManager.
        """

        super().__init__()

        self._masks = self._load_masks()

    def _load_masks(self):
        """
        gets all keywords that should be masked.

        :rtype: set[str]
        """

        normalized_defaults = self._normalize_case(self.DEFAULT_MASKED_KEYWORDS)
        include_defaults = config_services.get_active('logging.masking',
                                                      'include_default_keywords')
        extra_keywords = config_services.get_active('logging.masking', 'extra_keywords')
        extra_keywords = self._normalize_case(extra_keywords)

        results = []
        if include_defaults is True:
            results.extend(normalized_defaults)

        results.extend(extra_keywords)
        return set(results)

    def _normalize_case(self, items):
        """
        makes all items lowercase and returns a new list.

        :param list[str] | tuple[str] | set[str] items: items to be made lower case.

        :rtype: list[str]
        """

        results = []
        for item in items:
            results.append(item.lower())

        return results

    def should_mask(self, key):
        """
        gets a value indicating that given key should be masked in a dict.

        :param str key: dict key to be checked.

        :rtype: bool
        """

        if not isinstance(key, str):
            return False

        return key.lower() in self._masks

    def mask(self, data, **options):
        """
        masks the given data if required.

        if data is not a dict, no changes will be made.

        :param dict | object data: data to be masked.

        :returns: a masked dict or original input data.
        :rtype: MaskedDict | object
        """

        if isinstance(data, dict):
            return MaskedDict(data)

        return data
