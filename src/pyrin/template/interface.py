# -*- coding: utf-8 -*-
"""
template interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class TemplateHandlerSingletonMeta(MultiSingletonMeta):
    """
    template handler singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractTemplateHandler(CoreObject, metaclass=TemplateHandlerSingletonMeta):
    """
    abstract template handler class.
    """

    @abstractmethod
    def create(self, *args, **kwargs):
        """
        creates the template files in target path of this handler.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def name(self):
        """
        gets the name of this template handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()
