# -*- coding: utf-8 -*-
"""
hashing handlers base module.
"""

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class HashingBase(CoreObject):
    """
    hashing base class.
    all application hashing handlers must be subclassed from this.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of HashingBase.

        :param str name: name of the hashing handler.
        """

        CoreObject.__init__(self)

        self._set_name(name)

    def hash(self, value):
        """
        gets the hash of input value.

        :param str value: value to be hashed.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _get_algorithm(self):
        """
        gets the hashing algorithm.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

