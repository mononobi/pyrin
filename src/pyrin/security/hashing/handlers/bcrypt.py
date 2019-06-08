# -*- coding: utf-8 -*-
"""
bcrypt hashing handler module.
"""

import bcrypt

import pyrin.configuration.services as config_services

from pyrin.security.hashing.handlers.base import HashingBase
from pyrin.settings.static import APPLICATION_ENCODING


class BcryptHashing(HashingBase):
    """
    bcrypt hashing class.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of BcryptHashing.

        :param str name: name of the hashing handler.
        """

        # we pass the algorithm of hashing handler as the name of it.
        HashingBase.__init__(self, self._get_algorithm(), **options)

        self._set_name(name)

    def generate_hash(self, plain_text, salt):
        """
        gets the hash of input plain text and salt.

        :param str plain_text: text to be hashed.
        :param str salt: salt to append to plain text before hashing.

        :rtype: str
        """

        return bcrypt.hashpw(plain_text.encode(APPLICATION_ENCODING),
                             salt.encode(APPLICATION_ENCODING)).decode(APPLICATION_ENCODING)

    def generate_salt(self, **options):
        """
        generates a valid salt for this handler and returns it.

        :rtype: str
        """

        return bcrypt.gensalt(config_services.get('security', 'hashing', 'bcrypt_log_rounds'))

    def is_valid(self, plain_text, hashed_value):
        """
        gets a value indicating that given plain text's
        hash is identical to given hashed value.

        :param str plain_text: text to be hashed.
        :param str hashed_value: hashed value to compare with.

        :rtype: bool
        """

        return bcrypt.checkpw(plain_text, hashed_value)

    def _get_algorithm(self):
        """
        gets the hashing algorithm.

        :rtype: str
        """

        return 'bcrypt'
