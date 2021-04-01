# -*- coding: utf-8 -*-
"""
core globals module.
"""

from flask_babel import gettext
from sqlalchemy.engine import Row


class Constant:
    """
    constant class.

    this is a helper class for defining global constant objects.
    we have to declare this class in `globals` instead of `structs`
    to prevent circular dependency.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of Constant.

        :param str name: this constant's name.
        """

        super().__init__()
        self._name = name

    def __repr__(self):
        """
        gets the string representation of current constant.

        :rtype: str
        """

        return str(self)

    def __str__(self):
        """
        gets the string representation of current constant.

        :rtype: str
        """

        return self._name


# this value should be used as `None`, where the `None` itself has a meaning.
NULL = Constant('NULL')

# this value should be used where we need to reference class type of None objects.
NONE_TYPE = type(None)

# this value should be used where we want to determine if an object is a list type or not.
LIST_TYPES = (list, tuple, set)

# this method should be used for localizable strings.
_ = gettext

# this value should be used when working on Row objects.
ROW_RESULT = Row

# this value should be used instead of True when we want to preserve security of
# inputs which come from client to prevent injection of invalid values through options.
SECURE_TRUE = Constant('SECURE_TRUE')

# this value should be used instead of False when we want to preserve security of
# inputs which come from client to prevent injection of invalid values through options.
SECURE_FALSE = Constant('SECURE_FALSE')
