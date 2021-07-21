# -*- coding: utf-8 -*-
"""
admin interface module.
"""

import inspect

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.model.base import BaseEntity
from pyrin.admin.exceptions import InvalidAdminEntityTypeError, AdminNameRequiredError, \
    AdminRegisterNameRequiredError


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

    # ===================== REQUIRED CONFIGS ===================== #

    # the entity class that this admin page represents.
    entity = None

    # name of this admin page to be used for registration.
    # the register name is case-insensitive and must be unique for each admin page.
    register_name = None

    # name of this admin page for representation.
    name = None

    def __init__(self, *args, **options):
        """
        initializes an instance of AbstractAdminPage.

        :raises InvalidAdminEntityTypeError: invalid admin entity type error.
        :raises AdminRegisterNameRequiredError: admin register name required error.
        :raises AdminNameRequiredError: admin name required error.
        """

        super().__init__()

        if not inspect.isclass(self.entity) or not issubclass(self.entity, BaseEntity):
            raise InvalidAdminEntityTypeError('The entity for [{admin}] class '
                                              'must be a subclass of [{base}].'
                                              .format(admin=self, base=BaseEntity))

        if self.register_name in (None, '') or self.register_name.isspace():
            raise AdminRegisterNameRequiredError('The register name for '
                                                 '[{admin}] class is required.'
                                                 .format(admin=self))

        if self.name in (None, '') or self.name.isspace():
            raise AdminNameRequiredError('The name for [{admin}] class is required.'
                                         .format(admin=self))

    def get_register_name(self):
        """
        gets the register name of this admin page.

        :rtype: str
        """

        return self.register_name.lower()

    @abstractmethod
    def find(self, **filters):
        """
        finds entities with given filters.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: list[ROW_RESULT]
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def create(self, **data):
        """
        creates an entity with given data.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def update(self, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def remove(self, pk, **options):
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
