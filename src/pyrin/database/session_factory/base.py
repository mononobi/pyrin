# -*- coding: utf-8 -*-
"""
database session factory base module.
"""

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.interface import AbstractSessionFactoryBase


class SessionFactoryBase(AbstractSessionFactoryBase):
    """
    session factory base class.
    """

    def __init__(self, **options):
        """
        initializes an instance of SessionFactoryBase.
        """

        super().__init__()

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
