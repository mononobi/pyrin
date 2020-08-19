# -*- coding: utf-8 -*-
"""
logging masking manager module.
"""

from werkzeug.datastructures import Headers

import pyrin.configuration.services as config_services

from pyrin.core.structs import Manager
from pyrin.logging.masking import LoggingMaskingPackage
from pyrin.logging.masking.structs import MaskedDict


class LoggingMaskingManager(Manager):
    """
    logging masking manager class.
    """

    # these are default keywords that will be masked if they are present in a dict.
    # these values could be extended or disabled in 'logging.masking' config store.
    # note that all values will be normalized and matched against also normalized values.
    # for example 'api_key' and 'APIkey' and 'api-key' will be considered equal.
    DEFAULT_MASKED_KEYWORDS = {'access_token',
                               'address',
                               'api_key',
                               'api_token',
                               'auth_token',
                               'authentication',
                               'authorization',
                               'birth_certificate',
                               'birth_certificate_no',
                               'birth_certificate_number',
                               'birth_date',
                               'birthday',
                               'card_no',
                               'card_number',
                               'certificate',
                               'cookie',
                               'cookies',
                               'credential',
                               'credentials',
                               'credit_card',
                               'credit_card_no',
                               'credit_card_number',
                               'cvv',
                               'debit_card',
                               'debit_card_no',
                               'debit_card_number',
                               'email',
                               'email_address',
                               'fingerprint',
                               'hash',
                               'hash_value',
                               'home_address',
                               'http_auth',
                               'http_authorization',
                               'http_cookie',
                               'identity_code',
                               'identity_no',
                               'identity_number',
                               'mobile',
                               'mobile_no',
                               'mobile_number',
                               'national_code',
                               'national_no',
                               'national_number',
                               'oauth',
                               'oauth_token',
                               'otp',
                               'pass',
                               'passport',
                               'passport_no',
                               'passport_number',
                               'passwd',
                               'password',
                               'password_hash',
                               'phone',
                               'phone_no',
                               'phone_number',
                               'postal_address',
                               'postal_code',
                               'private_key',
                               'proxy_authorization',
                               'refresh_token',
                               'rsa',
                               'rsa_key',
                               'secret',
                               'secret_key',
                               'session',
                               'session_id',
                               'token',
                               'uploaded_files',
                               'username',
                               'www_authenticate',
                               'zip_code'}

    # a class type to be used as masked dict.
    masked_dict_class = MaskedDict
    package_class = LoggingMaskingPackage

    def __init__(self):
        """
        initializes an instance of LoggingMaskingManager.
        """

        super().__init__()

        self._masks = self._get_masked_keywords()

    def _get_masked_keywords(self):
        """
        gets all keywords that should be masked.

        :rtype: set[str]
        """

        normalized_defaults = self._normalize_items(self.DEFAULT_MASKED_KEYWORDS)
        include_defaults = config_services.get_active('logging.masking',
                                                      'include_default_keywords')
        extra_keywords = config_services.get_active('logging.masking', 'extra_keywords')
        extra_keywords = self._normalize_items(extra_keywords)

        results = list(extra_keywords)
        if include_defaults is True:
            results.extend(normalized_defaults)

        return set(results)

    def _normalize_items(self, items):
        """
        normalizes all given items and returns a new list.

        :param list[str] | tuple[str] | set[str] items: items to be normalized.

        :rtype: list[str]
        """

        results = []
        for item in items:
            results.append(self._normalize(item))

        return results

    def _normalize(self, value):
        """
        normalizes given value.

        if the value is not a string, it returns the value itself.
        this method does not check `isinstance` to detect strings, because it
        has a significant performance hit. so it returns the same value
        whenever an `AttributeError` is occurred.

        :param str | object value: value to be normalized.

        :rtype: str | object
        """

        try:
            return value.lower().replace('_', '').replace('-', '') \
                .replace('.', '').replace(' ', '')
        except AttributeError:
            return value

    def should_mask(self, key):
        """
        gets a value indicating that given key should be masked in a dict.

        :param str key: dict key to be checked.

        :rtype: bool
        """

        return self._normalize(key) in self._masks

    def mask(self, data, **options):
        """
        masks the given data if required.

        if data is not a dict, no changes will be made.

        :param dict | object data: data to be masked.

        :returns: a masked dict or original input data.
        :rtype: MaskedDict | object
        """

        if (isinstance(data, dict) and not
           isinstance(data, self.masked_dict_class)) or isinstance(data, Headers):
            return self.masked_dict_class(data)

        return data
