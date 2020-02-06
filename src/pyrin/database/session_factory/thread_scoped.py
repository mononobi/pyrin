# -*- coding: utf-8 -*-
"""
database thread_scoped session factory module.
"""

from sqlalchemy.orm import scoped_session, sessionmaker

import pyrin.configuration.services as config_services

from pyrin.database.decorators import session_factory
from pyrin.database.orm.query.base import CoreQuery
from pyrin.database.orm.session.base import CoreSession
from pyrin.database.session_factory.base import SessionFactoryBase


@session_factory()
class ThreadScopedSessionFactory(SessionFactoryBase):
    """
    thread scoped session factory class.
    """

    def __init__(self, **options):
        """
        initializes an instance of ThreadScopedSessionFactory.
        """

        super().__init__(**options)

    def _create_session_factory(self, engine):
        """
        creates a database thread scoped session factory and binds it to
        given engine and returns it. the scope is current thread.

        :param Engine engine: database engine.

        :returns: database session
        :rtype: Session
        """

        session_configs = config_services.get_section('database', 'thread_scoped_session')
        return scoped_session(sessionmaker(bind=engine, class_=CoreSession,
                                           query_cls=CoreQuery, **session_configs))

    def is_request_bounded(self):
        """
        gets a value determining that this session factory
        type should be bounded into request.

        :rtype: bool
        """

        return False
