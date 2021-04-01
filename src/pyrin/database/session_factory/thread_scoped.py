# -*- coding: utf-8 -*-
"""
database thread_scoped session factory module.
"""

from sqlalchemy.orm import sessionmaker

import pyrin.configuration.services as config_services

from pyrin.database.decorators import session_factory
from pyrin.database.orm.query.base import CoreQuery
from pyrin.database.orm.scoping.base import CoreScopedSession
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
        creates a database thread scoped session factory and binds it to given engine.

        the scope is current thread.

        :param Engine engine: database engine.

        :returns: database session
        :rtype: Session
        """

        session_configs = config_services.get_section('database', 'thread_scoped_session')
        return CoreScopedSession(sessionmaker(bind=engine, class_=CoreSession, future=True,
                                              query_cls=CoreQuery, **session_configs))

    @property
    def request_bounded(self):
        """
        gets a value indicating that this session factory type should be bounded into request.

        :rtype: bool
        """

        return False
