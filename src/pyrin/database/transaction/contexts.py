# -*- coding: utf-8 -*-
"""
transaction contexts module.
"""

from contextlib import AbstractContextManager

import pyrin.database.services as database_services


class atomic_context(AbstractContextManager):
    """
    atomic context manager to make a code block execution atomic.

    meaning that before starting the execution of the code, a new session with a
    new transaction will be started, and after the completion of that code, if it
    was successful, the new transaction will be committed or if it was not successful
    the new transaction will be rolled back without the consideration or affecting the
    parent transaction which by default is scoped to request. the corresponding new
    session will also be removed after code execution.

    note that it's not required to commit or rollback anything inside an atomic
    context, the `atomic` context manager will handle commit or rollback operations
    when needed.

    also note that you *should not* remove the corresponding session from session factory
    when using `atomic` context. the removal operation will be handled by context manager
    itself and if you remove session manually, it will cause broken chain of sessions
    and unexpected behaviour.

    this context manager also supports multiple `atomic` usage in a single call hierarchy.
    for example:

    def service_root():
        store = get_current_store()
        value = EntityRoot()
        store.add(value)
        service_a()

    def service_a():
        with atomic_context() as store:
            value = EntityA()
            store.add(value)
            service_b()
            raise Exception()

    def service_b():
        with atomic_context() as store:
            value = EntityB()
            store.add(value)
            service_c()

    def service_c():
        with atomic_context():
            value = EntityC()
            value.save()

    in the above example, if the call hierarchy starts with `service_root()`, at
    the end, the data of `service_c` and `service_b` will be persisted into database.
    but the data of `service_a` and `service_root` will not be persisted because
    `service_a` raises an error before finish.
    """

    def __init__(self):
        """
        initializes an instance of atomic_context.
        """

        self._store = database_services.get_atomic_store()

    def __enter__(self):
        """
        begins the current context and returns the atomic session for current context.

        example usage:

        with atomic_context() as store:
            user = UserEntity(id=1, name='Dave')
            store.add(user)

        or you could get the current store inside the block, it
        will always give you the correct session:

        with atomic_context():
            store = database_services.get_current_store()
            user = UserEntity(id=1, name='Dave')
            store.add(user)

        note that there is no need to commit or rollback the transaction inside
        the current context, the `atomic` context manager will do it automatically.

        :rtype: CoreSession
        """

        return self._store

    def __exit__(self, exc_type, exc_value, traceback):
        """
        does the finalizing of atomic transaction.

        it commits the transaction if it was successful, otherwise rollbacks it.

        :param type[Exception] exc_type: the exception type that has been
                                         occurred during current context.

        :param Exception exc_value: exception instance that has been
                                    occurred during current context.

        :param traceback traceback: traceback of occurred exception.
        """

        try:
            if exc_type is None:
                try:
                    self._store.commit()
                except Exception as error:
                    self._store.rollback()
                    raise error
                finally:
                    self._remove_session()
            else:
                try:
                    self._store.rollback()
                finally:
                    self._remove_session()
        except Exception as error:
            if exc_type is None or type(error) is not exc_type:
                raise error

    def _remove_session(self):
        """
        removes the current atomic session from session factory.
        """

        factory = database_services.get_current_session_factory()
        factory.remove(atomic=True)
