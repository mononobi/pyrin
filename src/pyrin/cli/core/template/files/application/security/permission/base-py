# -*- coding: utf-8 -*-
"""
permission base module.
"""

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.permission.base import PermissionBase


class Permission(PermissionBase):
    """
    permission class.

    all application permissions must be an instance of this.
    """

    def __init__(self, *args, **options):
        """
        initializes an instance of Permission.

        input parameters of this method must be customized
        based on your application's design requirements.
        """

        # set the required attributes and check validations here, above the `super()` call.

        super().__init__(*args, **options)

    def __str__(self):
        """
        gets the string representation of current permission.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def to_entity(self):
        """
        gets the equivalent entity of current permission.

        :rtype: BaseEntity
        """

        raise CoreNotImplementedError()

    def get_id(self):
        """
        gets permission id.

        it could return a single value or a combination of multiple values
        (ex. a tuple). note that the returned value must be fully unique for
        each different permission and also it must be a hashable value to
        be used as dict key.

        :rtype: object
        """

        raise CoreNotImplementedError()
