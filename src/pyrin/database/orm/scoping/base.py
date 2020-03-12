# -*- coding: utf-8 -*-
"""
orm scoping base module.
"""

from sqlalchemy.orm import scoped_session
from sqlalchemy.util import warn

from pyrin.database.orm.scoping.registry.request_scoped import RequestScopedRegistry
from pyrin.database.orm.scoping.registry.thread_scoped import ThreadScopedRegistry


class CoreScopedSession(scoped_session):
    """
    core scoped session class.

    this class is subclassed from `scoped_session` to provide a way to overcome
    out of request context error when configuring sessions on server startup.
    """

    def __init__(self, session_factory, scopefunc=None):
        """
        initializes an instance of CoreScopedSession.

        :param Session session_factory: a factory to create new `Session`
                                        instances. this is usually, but not
                                        necessarily, an instance of `sessionmaker`.

        :param callable scopefunc: optional function which defines the current scope.
                                   if not passed, the `scoped_session` class object
                                   assumes `thread-local` scope, and will use a python
                                   `threading.local()` in order to maintain the current
                                   `Session`. if passed, the function should return a
                                   hashable token. this token will be used as the key
                                   in a dictionary in order to store and retrieve the
                                   current `Session`.
        """

        self.session_factory = session_factory

        if scopefunc:
            self.registry = RequestScopedRegistry(session_factory, scopefunc)
        else:
            self.registry = ThreadScopedRegistry(session_factory)

    def configure(self, **kwargs):
        """
        reconfigures the `sessionmaker` used by this `CoreScopedSession`.

        this method is overridden to use `safe_has()` to prevent
        errors when the scope function is not ready yet.
        """

        if self.registry.safe_has():
            warn('At least one scoped session is already present. '
                 'configure() can not affect sessions that have '
                 'already been created.')

        self.session_factory.configure(**kwargs)
