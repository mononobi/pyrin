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

        :rtype: type[pyrin.database.model.base.BaseEntity]
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
    def get_plural_name(self):
        """
        gets the plural name of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_singular_name(self):
        """
        gets the singular name of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get(self, pk):
        """
        gets an entity with given primary key.

        :param object pk: primary key of entity to be get.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: pyrin.database.model.base.BaseEntity
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

    @classmethod
    @abstractmethod
    def create(cls, **data):
        """
        creates an entity with given data.

        it's preferred for this method to return the pk of created entity
        if it is not a composite primary key. this lets the client to fill
        fk fields automatically after create.

        :keyword **data: all data to be passed to related create service.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    @classmethod
    @abstractmethod
    def update(cls, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related update service.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @classmethod
    @abstractmethod
    def remove(cls, pk):
        """
        deletes an entity with given pk.

        :param object pk: entity primary key to be deleted.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def remove_bulk(self, pk):
        """
        deletes entities with given primary keys.

        :param object | list[object] pk: entity primary keys to be deleted.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def remove_all(self):
        """
        deletes all entities.

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

    @abstractmethod
    def has_get_permission(self):
        """
        gets a value indicating that this admin page has get permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def has_create_permission(self):
        """
        gets a value indicating that this admin page has create permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def has_update_permission(self):
        """
        gets a value indicating that this admin page has update permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def has_remove_permission(self):
        """
        gets a value indicating that this admin page has single or bulk remove permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def has_remove_all_permission(self):
        """
        gets a value indicating that this admin page has remove all permission.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_main_metadata(self):
        """
        gets the main metadata of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_find_metadata(self):
        """
        gets the find metadata of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_create_metadata(self):
        """
        gets the create metadata of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_update_metadata(self):
        """
        gets the update metadata of this admin page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def populate_caches(self):
        """
        populates required caches of this admin page.

        :raises CoreNotImplementedError: core not implemented error.
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
