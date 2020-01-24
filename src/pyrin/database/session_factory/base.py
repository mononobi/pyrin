# -*- coding: utf-8 -*-
"""
database session factory base module.
"""

from threading import Lock

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utils.singleton import MultiSingletonMeta


class SessionFactorySingletonMeta(MultiSingletonMeta):
    """
    session factory singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    # a dictionary containing an instance of each type.
    # in the form of: {type: instance}
    _instances = dict()
    _lock = Lock()


class SessionFactoryBase(CoreObject, metaclass=SessionFactorySingletonMeta):
    """
    session factory base class.
    """

    def __init__(self, **options):
        """
        initializes an instance of SessionFactoryBase.
        """

        CoreObject.__init__(self)

    def create_session_factory(self, engine):
        """
        creates a database session factory and binds it to
        given engine and returns it.

        :param Engine engine: database engine.

        :returns: database session
        :rtype: Session
        """

        session = self._create_session_factory(engine)
        setattr(session, 'session_factory_name', self.get_name())
        setattr(session, 'is_request_bounded', self.is_request_bounded())
        return session

    def _create_session_factory(self, engine):
        """
        creates a database session factory and binds it to
        given engine and returns it.

        :param Engine engine: database engine.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: database session
        :rtype: Session
        """

        raise CoreNotImplementedError()

    def is_request_bounded(self):
        """
        gets a value indicating that this session factory
        type should be bounded into request.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
