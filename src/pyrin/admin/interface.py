# -*- coding: utf-8 -*-
"""
admin interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class AdminPageSingletonMeta(MultiSingletonMeta):
    """
    admin page singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractAdminPage(CoreObject, metaclass=AdminPageSingletonMeta):
    """
    abstract admin page class.
    """

    @abstractmethod
    def get_entity(self):
        """
        gets the entity class of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: pyrin.database.model.base.BaseEntity
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_register_name(self):
        """
        gets the register name of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_category(self):
        """
        gets the category of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def find(self, **filters):
        """
        finds entities with given filters.

        :keyword **filters: all filters to be passed to related find service.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: list[ROW_RESULT]
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def create(self, **data):
        """
        creates an entity with given data.

        :keyword **data: all data to be passed to related create service.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def update(self, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related update service.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def remove(self, pk):
        """
        deletes an entity with given pk.

        :param object pk: entity primary key to be deleted.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def call_method(self, name, argument):
        """
        calls the method with given name with given argument and returns the result.

        :param str name: method name.
        :param ROW_RESULT argument: the method argument.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def method_names(self):
        """
        gets the list of all method names of this admin page to be used for result processing.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: tuple[str]
        """

        raise CoreNotImplementedError()
