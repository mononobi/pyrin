# -*- coding: utf-8 -*-
"""
transaction contexts module.
"""

import pyrin.database.services as database_services

from pyrin.core.contexts import ContextManagerBase


class TransactionalContextManagerBase(ContextManagerBase):
    """
    transactional context manager base class.

    this class should be used as the base for all transactional context managers.
    """

    def __init__(self, store, **options):
        """
        initializes an instance of TransactionalContextManagerBase.

        :param CoreSession store: the session object for current context.
        """

        self._store = store

    def __enter__(self):
        """
        begins the current context and returns the related session for current context.

        note that you *should not* commit, flush or rollback the transaction inside
        the current context. the context manager itself will do it automatically.
        if you do commit, flush or rollback manually, unexpected behaviors may occur.

        :rtype: CoreSession
        """

        return self._store

    def __exit__(self, exc_type, exc_value, traceback):
        """
        does the finalizing of current transaction.

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
            else:
                self._store.rollback()
        except Exception as error:
            if self._should_be_raised(error, exc_type) is True:
                raise error


class atomic_context(TransactionalContextManagerBase):
    """
    atomic context manager to make a code block execution atomic.

    meaning that before starting the execution of the code, a new session with a
    new transaction will be started, and after the completion of that code, if it
    was successful, the new transaction will be committed or if it was not successful
    the new transaction will be rolled back without the consideration or affecting the
    parent transaction which by default is scoped to request. the corresponding new
    session will also be removed after code execution.

    note that you *should not* commit, flush or rollback the transaction inside
    the current context. the context manager itself will do it automatically.
    if you do commit, flush or rollback manually, unexpected behaviors may occur.

    also note that you *should not* remove the corresponding session from session factory
    when using `atomic_context`. the removal operation will be handled by context manager
    itself and if you remove session manually, it will cause broken chain of sessions
    and unexpected behaviour.

    this context manager also supports multiple `atomic_context` usage in a single
    call hierarchy.

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

    def __init__(self, **options):
        """
        initializes an instance of atomic_context.

        :keyword bool expire_on_commit: expire atomic session after commit.
                                        it is useful to set it to True if
                                        the atomic function does not return
                                        any entities for post-processing.
                                        defaults to False if not provided.
        """

        super().__init__(database_services.get_atomic_store(**options))

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
            try:
                super().__exit__(exc_type, exc_value, traceback)
            finally:
                self._remove_session()
        except Exception as error:
            if self._should_be_raised(error, exc_type) is True:
                raise error

    def _remove_session(self):
        """
        removes the current atomic session from session factory.
        """

        factory = database_services.get_current_session_factory()
        factory.remove(atomic=True)


class nested_context(TransactionalContextManagerBase):
    """
    nested context manager to make a code block executed in nested transaction.

    meaning that before starting the execution of the code, a new nested transaction
    will be started, and after the completion of that code, if it was not successful
    the nested transaction will be rolled back without the consideration or affecting
    the parent transaction which by default is scoped to request.

    note that in nested transactions, the parent transaction must be committed to persist
    generated data during nested transaction, so committing the nested transaction itself,
    does not persist anything, it just releases the savepoint. if you want an independent
    transaction from parent that could commit its own changes on its own, use `atomic_context`.

    note that you *should not* commit, flush or rollback the transaction inside
    the current context. the context manager itself will do it automatically.
    if you do commit, flush or rollback manually, unexpected behaviors may occur.

    this context manager also supports multiple `nested_context` usage in a single
    call hierarchy.

    example usage:

    with nested_context():
        store = database_services.get_current_store()
        user = UserEntity(id=1, name='Dave')
        store.add(user)
    """

    def __init__(self):
        """
        initializes an instance of nested_context.
        """

        super().__init__(database_services.get_current_store().begin_nested())

    def __enter__(self):
        """
        begins the current context.

        note that you *should not* commit, flush or rollback the transaction inside
        the current context. the context manager itself will do it automatically.
        if you do commit, flush or rollback manually, unexpected behaviors may occur.

        also note that by beginning the context, it does not return any session
        object. so you should not use `with nested_context() as store` code style.
        because store will always be None.

        :rtype: CoreSession
        """

        return None


class subtransaction_context(TransactionalContextManagerBase):
    """
    subtransaction context manager to make a code block executed in subtransaction.

    meaning that before starting the execution of the code, a new subtransaction
    will be started, and after the completion of that code, if it was not successful
    the subtransaction will be rolled back and it will also force the parent transaction
    which by default is scoped to request to be rolled backed.

    note that in subtransactions, the parent transaction must be committed to persist
    generated data during subtransaction, so committing the subtransaction itself, does
    not persist anything, it just ends the subtransaction's scope. if you want an independent
    transaction from parent that could commit its own changes on its own, use `atomic_context`.

    note that you *should not* commit, flush or rollback the transaction inside
    the current context. the context manager itself will do it automatically.
    if you do commit, flush or rollback manually, unexpected behaviors may occur.

    this context manager also supports multiple `subtransaction_context` usage in a single
    call hierarchy.

    example usage:

    with subtransaction_context():
        store = database_services.get_current_store()
        user = UserEntity(id=1, name='Dave')
        store.add(user)
    """

    def __init__(self):
        """
        initializes an instance of subtransaction_context.
        """

        super().__init__(database_services.get_current_store().begin(subtransactions=True))

    def __enter__(self):
        """
        begins the current context.

        note that you *should not* commit, flush or rollback the transaction inside
        the current context. the context manager itself will do it automatically.
        if you do commit, flush or rollback manually, unexpected behaviors may occur.

        also note that by beginning the context, it does not return any session
        object. so you should not use `with subtransaction_context() as store` code
        style. because store will always be None.

        :rtype: CoreSession
        """

        return None


class transient_context(atomic_context):
    """
    transient context manager to make a code block execution transient.

    meaning that before starting the execution of the code block, a new session with a
    new transaction will be started, and after the completion of that code, the
    new transaction will be rolled back without the consideration or affecting the
    parent transaction which by default is scoped to request. the corresponding new
    session will also be removed after code execution.

    note that you *should not* commit, flush or rollback anything inside a transient
    block, the transient context manager will handle rollback operation when needed.
    otherwise, unexpected behaviors may occur.

    also note that you *should not* remove the corresponding session from session factory
    when using transient context manager. the removal operation will be handled by decorator
    itself and if you remove session manually, it will cause broken chain of sessions
    and unexpected behaviour.

    this context manager also supports multiple `transient_context` usage in a single
    call hierarchy.

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

    def service_b():
        with transient_context() as store:
            value = EntityB()
            store.add(value)
            service_c()

    def service_c():
        with transient_context():
            value = EntityC()
            value.save()

    in the above example, if the call hierarchy starts with `service_root()`, at
    the end, the data of `service_root` and `service_a` will be persisted into database.
    but the data of `service_b` and `service_c` will not be persisted because
    they are marked as transient.
    """

    def __exit__(self, exc_type, exc_value, traceback):
        """
        does the finalizing of transient transaction.

        it rollbacks the transaction at the end.

        :param type[Exception] exc_type: the exception type that has been
                                         occurred during current context.

        :param Exception exc_value: exception instance that has been
                                    occurred during current context.

        :param traceback traceback: traceback of occurred exception.
        """

        try:
            try:
                self._store.rollback()
            finally:
                self._remove_session()
        except Exception as error:
            if self._should_be_raised(error, exc_type) is True:
                raise error
