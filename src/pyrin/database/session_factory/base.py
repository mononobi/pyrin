# -*- coding: utf-8 -*-
"""
database session factory base module.
"""

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class SessionFactoryBase(CoreObject):
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
