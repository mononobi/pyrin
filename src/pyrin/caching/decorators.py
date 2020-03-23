# -*- coding: utf-8 -*-
"""
caching decorators module.
"""


# def atomic(*old_func, auto_commit=True):
#     """
#     decorator to make a function execution atomic.
#
#     meaning that before starting the execution of the function, a new session with a
#     new transaction will be started, and after the completion of that function, if it
#     was successful, the new transaction will be committed or if it was not successful
#     the new transaction will be rolled back without the consideration or affecting the
#     parent transaction which by default is scoped to request. the corresponding new
#     session will also be removed after function execution.
#
#     this decorator supports with or without argument usage.
#     for example: `@atomic` or `@atomic(auto_commit=False)`
#
#     :param bool auto_commit: specifies that the result of the function must be
#                              auto committed. defaults to True if not provided.
#
#     :returns: function result.
#     """
#
#     def decorator(func):
#         """
#         decorates the given function and makes its execution atomic.
#
#         :param function func: function.
#
#         :returns: function result.
#         """
#
#         def wrapper(*args, **kwargs):
#             """
#             decorates the given function and makes its execution atomic.
#
#             :param object args: function arguments.
#             :param object kwargs: function keyword arguments.
#
#             :returns: function result.
#             """
#
#             store = database_services.get_atomic_store()
#             try:
#                 result = func(*args, **kwargs)
#                 if auto_commit is True:
#                     store.commit()
#                 return result
#             except Exception as ex:
#                 store.rollback()
#                 raise ex
#             finally:
#                 if auto_commit is True:
#                     factory = database_services.get_current_session_factory()
#                     factory.remove(True)
#
#         return update_wrapper(wrapper, func)
#
#     if len(old_func) > 0:
#         return decorator(old_func[0])
#
#     return decorator
