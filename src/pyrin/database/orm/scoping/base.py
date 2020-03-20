# -*- coding: utf-8 -*-
"""
orm scoping base module.
"""

from sqlalchemy.orm import scoped_session

from pyrin.database.orm.scoping.interface import AbstractScopedRegistryBase
from pyrin.database.orm.scoping.registry.request_scoped import RequestScopedRegistry
from pyrin.database.orm.scoping.registry.thread_scoped import ThreadScopedRegistry
from pyrin.database.orm.scoping.exceptions import InvalidRequestScopedRegistryTypeError, \
    InvalidThreadScopedRegistryTypeError, ScopedSessionIsAlreadyPresentError


class CoreScopedSession(scoped_session):
    """
    core scoped session class.

    it also supports atomic sessions.
    """

    def __init__(self, session_factory, scopefunc=None,
                 request_registry=RequestScopedRegistry,
                 thread_registry=ThreadScopedRegistry):
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

        :param type[AbstractScopedRegistryBase] request_registry: registry type to be used
                                                                  for request scoped sessions.
                                                                  defaults to
                                                                  `RequestScopedRegistry`
                                                                  if not provided.

        :param type[AbstractScopedRegistryBase] thread_registry: registry type to be used
                                                                 for thread scoped sessions.
                                                                 defaults to
                                                                 `ThreadScopedRegistry`
                                                                 if not provided.

        :raises InvalidRequestScopedRegistryTypeError: invalid request scoped
                                                       registry type error.

        :raises InvalidThreadScopedRegistryTypeError: invalid thread scoped
                                                      registry type error.
        """

        self.session_factory = session_factory

        message = 'Input parameter [{type_}] is not a subclass of [{base}].'
        if request_registry is None or not issubclass(request_registry,
                                                      AbstractScopedRegistryBase):

            raise InvalidRequestScopedRegistryTypeError(message
                                                        .format(type_=request_registry,
                                                                base=AbstractScopedRegistryBase))

        if thread_registry is None or not issubclass(thread_registry,
                                                     AbstractScopedRegistryBase):

            raise InvalidThreadScopedRegistryTypeError(message
                                                       .format(type_=thread_registry,
                                                               base=AbstractScopedRegistryBase))

        if scopefunc:
            self.registry = request_registry(session_factory, scopefunc)
        else:
            self.registry = thread_registry(session_factory)

    def __call__(self, atomic=False, **kw):
        """
        gets the current `Session` object.

        creating it using the `CoreScopedSession.session_factory` if not present.

        :param bool atomic: specifies that it must get an atomic session.
                            it returns it from atomic registry if available,
                            otherwise gets a new atomic session.
                            defaults to False if not provided.

        :keyword object **kw: keyword arguments will be passed to the
                              `CoreScopedSession.session_factory` callable,
                              if an existing `Session` is not present. if
                              the `.Session` is present and keyword arguments
                              have been passed, `sqlalchemy.exc.InvalidRequestError`
                              is raised.

        :raises ScopedSessionIsAlreadyPresentError: scoped session is already present error.

        :rtype: CoreSession
        """

        if kw:
            has_atomic = self.registry.has(True)
            has = self.registry.has()

            if has_atomic is True or (atomic is False and has is True):
                raise ScopedSessionIsAlreadyPresentError('Scoped session is already present, '
                                                         'no new arguments may be specified.')
            else:
                session = self.session_factory(**kw)
                self.registry.set(session, atomic)
                return session
        else:
            return self.registry(atomic)

    def remove(self, atomic=False):
        """
        disposes the current `Session` objects of current scope, if present.

        this will first call `Session.close` method on the current `Session`,
        which releases any existing transactional/connection resources still
        being held. transactions specifically are rolled back. the `Session`
        is then discarded. upon next usage within the same scope, the
        `CoreScopedSession` will produce a new `Session` object.

        :param bool atomic: specifies that it must only dispose an atomic session
                            of current scope. otherwise, it disposes all sessions
                            of current scope. defaults to False if not provided.
        """

        self._remove_atomic()
        if atomic is False:
            self._remove()

    def _remove(self):
        """
        disposes the current normal `Session` object of current scope, if present.

        this will first call `Session.close` method on the current `Session`,
        which releases any existing transactional/connection resources still
        being held. transactions specifically are rolled back. the `Session`
        is then discarded. upon next usage within the same scope, the
        `CoreScopedSession` will produce a new `Session` object.
        """

        session = self.registry.get()
        if session is not None:
            session.close()
        self.registry.clear()

    def _remove_atomic(self):
        """
        disposes the current atomic `Session` object of current scope, if present.

        this will first call `Session.close` method on the current `Session`,
        which releases any existing transactional/connection resources still
        being held. transactions specifically are rolled back. the `Session`
        is then discarded. upon next usage within the same scope, the
        `CoreScopedSession` will produce a new atomic `Session` object.
        """

        atomic_session = self.registry.get(True)
        if atomic_session is not None:
            atomic_session.close()
        self.registry.clear(True)

    def commit_all(self, atomic=False):
        """
        commits all sessions related to current scope.

        note that current scope could have at most two current
        sessions, a normal session and an atomic session.

        :param bool atomic: specifies that it must only commit the atomic session of current
                            scope. otherwise, it commits all sessions of current scope.
                            defaults to False if not provided.
        """

        self._commit_atomic()
        if atomic is False:
            self._commit()

    def _commit(self):
        """
        commits the normal session of current scope, if available.

        note that current scope could have at most one normal
        session at the same time.
        """

        session = self.registry.get()
        if session is not None:
            session.commit()

    def _commit_atomic(self):
        """
        commits the atomic session of current scope, if available.

        note that current scope could have at most one atomic
        session at the same time.
        """

        atomic_session = self.registry.get(True)
        if atomic_session is not None:
            atomic_session.commit()

    def rollback_all(self, atomic=False):
        """
        rollbacks all sessions related to current scope.

        note that current scope could have at most two current
        sessions, a normal session and an atomic session.

        :param bool atomic: specifies that it must only rollback the atomic session of current
                            scope. otherwise, it commits all sessions of current scope.
                            defaults to False if not provided.
        """

        self._rollback_atomic()
        if atomic is False:
            self._rollback()

    def _rollback(self):
        """
        rollbacks the normal session of current scope, if available.

        note that current scope could have at most one normal
        session at the same time.
        """

        session = self.registry.get()
        if session is not None:
            session.rollback()

    def _rollback_atomic(self):
        """
        rollbacks the atomic session of current scope, if available.

        note that current scope could have at most one atomic
        session at the same time.
        """

        atomic_session = self.registry.get(True)
        if atomic_session is not None:
            atomic_session.rollback()
