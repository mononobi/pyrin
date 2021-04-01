# -*- coding: utf-8 -*-
"""
transaction decorators module.
"""

from functools import update_wrapper

import pyrin.database.services as database_services


def atomic(*old_func, **options):
    """
    decorator to make a function execution atomic.

    meaning that before starting the execution of the function, a new session with a
    new transaction will be started, and after the completion of that function, if it
    was successful, the new transaction will be committed or if it was not successful
    the new transaction will be rolled back without the consideration or affecting the
    parent transaction which by default is scoped to request. the corresponding new
    session will also be removed after function execution.

    note that you *should not* commit, flush or rollback anything inside an atomic
    function, the `@atomic` decorator will handle commit, flush or rollback operations
    when needed. otherwise, unexpected behaviors may occur.

    also note that you *should not* remove the corresponding session from session factory
    when using `@atomic` decorator. the removal operation will be handled by decorator
    itself and if you remove session manually, it will cause broken chain of sessions
    and unexpected behaviour.

    this decorator also supports multiple `@atomic` usage in a single call hierarchy.
    for example:

    def service_root():
        store = get_current_store()
        value = EntityRoot()
        store.add(value)
        service_a()

    @atomic
    def service_a():
        store = get_current_store()
        value = EntityA()
        store.add(value)
        service_b()
        raise Exception()

    @atomic
    def service_b():
        store = get_current_store()
        value = EntityB()
        store.add(value)
        service_c()

    @atomic
    def service_c():
        value = EntityC()
        value.save()

    in the above example, if the call hierarchy starts with `service_root()`, at
    the end, the data of `service_c` and `service_b` will be persisted into database.
    but the data of `service_a` and `service_root` will not be persisted because
    `service_a` raises an error before finish.

    :param function old_func: function.

    :keyword bool expire_on_commit: expire atomic session after commit.
                                    it is useful to set it to True if
                                    the atomic function does not return
                                    any entities for post-processing.
                                    defaults to False if not provided.

    :returns: function result.
    """

    def decorator(func):
        """
        decorates the given function and makes its execution atomic.

        :param function func: function.

        :returns: decorated function
        """

        def wrapper(*args, **kwargs):
            """
            decorates the given function and makes its execution atomic.

            :param object args: function arguments.
            :param object kwargs: function keyword arguments.

            :returns: function result.
            """

            store = database_services.get_atomic_store(**options)
            try:
                result = func(*args, **kwargs)
                store.commit()
                return result
            except Exception as ex:
                store.rollback()
                raise ex
            finally:
                factory = database_services.get_current_session_factory()
                factory.remove(atomic=True)

        return update_wrapper(wrapper, func)

    if len(old_func) > 0:
        return decorator(old_func[0])

    return decorator


def nested(func):
    """
    decorator to execute a function in a nested transaction.

    meaning that before starting the execution of the function, a new nested transaction
    will be started, and after the completion of that function, if it was not successful
    the nested transaction will be rolled back without the consideration or affecting
    the parent transaction which by default is scoped to request.

    note that in nested transactions, the parent transaction must be committed to persist
    generated data during nested transaction, so committing the nested transaction itself,
    does not persist anything, it just releases the savepoint. if you want an independent
    transaction from parent that could commit its own changes on its own, use `@atomic`
    decorator.

    note that you *should not* commit, flush or rollback anything inside a nested
    function, the `@nested` decorator will handle commit, flush or rollback operations
    when needed. otherwise, unexpected behaviors may occur.

    :param function func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and executes it in a nested transaction.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        store = database_services.get_current_store()
        nested_transaction = store.begin_nested()
        try:
            result = func(*args, **kwargs)
            nested_transaction.commit()
            return result
        except Exception as ex:
            nested_transaction.rollback()
            raise ex

    return update_wrapper(decorator, func)


def subtransaction(func):
    """
    decorator to execute a function in a subtransaction.

    meaning that before starting the execution of the function, a new subtransaction
    will be started, and after the completion of that function, if it was not successful
    the subtransaction will be rolled back and it will also force the parent transaction
    which by default is scoped to request to be rolled backed.

    note that in subtransactions, the parent transaction must be committed to persist
    generated data during subtransaction, so committing the subtransaction itself, does
    not persist anything, it just ends the subtransaction's scope. if you want an independent
    transaction from parent that could commit its own changes on its own, use `@atomic`
    decorator.

    note that you *should not* commit, flush or rollback anything inside a subtransaction
    function, the `@subtransaction` decorator will handle commit, flush or rollback
    operations when needed. otherwise, unexpected behaviors may occur.

    :param function func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and executes it in a subtransaction.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        store = database_services.get_current_store()
        sub_transaction = store.begin(subtransactions=True)
        try:
            result = func(*args, **kwargs)
            sub_transaction.commit()
            return result
        except Exception as ex:
            sub_transaction.rollback()
            raise ex

    return update_wrapper(decorator, func)


def transient(func):
    """
    decorator to make a function execution transient.

    meaning that before starting the execution of the function, a new session with a
    new transaction will be started, and after the completion of that function, the
    new transaction will be rolled back without the consideration or affecting the
    parent transaction which by default is scoped to request. the corresponding new
    session will also be removed after function execution.

    note that you *should not* commit, flush or rollback anything inside a transient
    function, the `@transient` decorator will handle rollback operation when needed.
    otherwise, unexpected behaviors may occur.

    also note that you *should not* remove the corresponding session from session factory
    when using `@transient` decorator. the removal operation will be handled by decorator
    itself and if you remove session manually, it will cause broken chain of sessions
    and unexpected behaviour.

    this decorator also supports multiple `@transient` usage in a single call hierarchy.
    for example:

    def service_root():
        store = get_current_store()
        value = EntityRoot()
        store.add(value)
        service_a()

    @atomic
    def service_a():
        store = get_current_store()
        value = EntityA()
        store.add(value)
        service_b()

    @transient
    def service_b():
        store = get_current_store()
        value = EntityB()
        store.add(value)
        service_c()

    @transient
    def service_c():
        value = EntityC()
        value.save()

    in the above example, if the call hierarchy starts with `service_root()`, at
    the end, the data of `service_root` and `service_a` will be persisted into database.
    but the data of `service_b` and `service_c` will not be persisted because they are
    decorated as transient.

    :param function func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and makes its execution transient.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        store = database_services.get_atomic_store()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            store.rollback()
            factory = database_services.get_current_session_factory()
            factory.remove(atomic=True)

    return update_wrapper(decorator, func)
