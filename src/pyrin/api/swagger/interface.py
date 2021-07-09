# -*- coding: utf-8 -*-
"""
swagger interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class TagSingletonMeta(MultiSingletonMeta):
    """
    tag singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractTag(CoreObject, metaclass=TagSingletonMeta):
    """
    abstract tag class.
    """

    # name of this tag to be registered with.
    _name = None

    # tag name of this tag to be used in swagger ui.
    _tag = None

    @abstractmethod
    def is_accepted(self, rule, method, **options):
        """
        gets a value indicating that this rule is accepted for this tag.

        :param pyrin.api.router.handlers.base.RouteBase rule: rule instance to be processed.
        :param str method: http method name.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def name(self):
        """
        gets the name of this tag.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        return self._name

    @property
    @abstractmethod
    def tag(self):
        """
        gets the tag name of this tag.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        return self._tag
