# -*- coding: utf-8 -*-
"""
mimetype manager module.
"""

from pyrin.core.structs import Manager, Context
from pyrin.processor.mimetype import MIMETypePackage
from pyrin.processor.mimetype.interface import AbstractMIMETypeHandlerBase
from pyrin.utils.custom_print import print_warning
from pyrin.processor.mimetype.exceptions import InvalidMIMETypeHandlerTypeError, \
    DuplicatedMIMETypeHandlerError


class MIMETypeManager(Manager):
    """
    mimetype manager class.
    """

    package_class = MIMETypePackage

    def __init__(self):
        """
        initializes an instance of MIMETypeManager.
        """

        super().__init__()

        # a dictionary containing information of registered mimetype handlers.
        # example: dict(type accepted_type: list[AbstractMIMETypeHandlerBase] instances)
        self._handlers = Context()

    def get_mimetype(self, value, **options):
        """
        gets the mimetype of given value.

        returns None if it could not detect the correct mimetype.

        :param object value: value to detect its mimetype.

        :returns: mimetype name
        :rtype: str
        """

        options.update(accepted_type=type(value))
        for handler in self.get_mimetype_handlers(**options):
            mimetype = handler.mimetype(value, **options)
            if mimetype is not None:
                return mimetype
            continue

        return None

    def register_mimetype_handler(self, instance, **options):
        """
        registers a new mimetype handler or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a mimetype handler which is already registered.

        :param AbstractMIMETypeHandlerBase instance: mimetype handler to be registered.
                                                     it must be an instance of
                                                     AbstractMIMETypeHandlerBase.

        :keyword bool replace: specifies that if there is another registered
                               mimetype handler with the same name and accepted type,
                               replace it with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidMIMETypeHandlerTypeError: invalid mimetype handler type error.
        :raises DuplicatedMIMETypeHandlerError: duplicated mimetype handler error.
        """

        if not isinstance(instance, AbstractMIMETypeHandlerBase):
            raise InvalidMIMETypeHandlerTypeError('Input parameter [{instance}] is '
                                                  'not an instance of [{base}].'
                                                  .format(instance=instance,
                                                          base=InvalidMIMETypeHandlerTypeError))

        previous_instances = self._handlers.get(instance.accepted_type, [])
        if instance.accepted_type in self._handlers:
            if len(previous_instances) > 0:
                old_instance = self._get_mimetype_handler_with_name(instance.get_name(),
                                                                    previous_instances)
                if old_instance is not None:
                    replace = options.get('replace', False)
                    if replace is not True:
                        raise DuplicatedMIMETypeHandlerError('There is another registered '
                                                             'mimetype handler with name '
                                                             '[{name}] for accepted type '
                                                             '[{accepted_type}] but "replace" '
                                                             'option is not set, so mimetype '
                                                             'handler [{instance}] could not '
                                                             'be registered.'
                                                             .format(name=instance.get_name(),
                                                                     accepted_type=instance.
                                                                     accepted_type,
                                                                     instance=instance))

                    print_warning('MIMEType handler [{old_instance}] is going '
                                  'to be replaced by [{new_instance}].'
                                  .format(old_instance=old_instance,
                                          new_instance=instance))

                    previous_instances.remove(old_instance)

        previous_instances.append(instance)
        self._set_next_handlers(previous_instances)
        self._handlers[instance.accepted_type] = previous_instances

    def _set_next_handlers(self, mimetype_handlers):
        """
        sets next handler for each mimetype handler in the input list.

        :param list[AbstractMIMETypeHandlerBase] mimetype_handlers: list of mimetype handlers.
        """

        length = len(mimetype_handlers)
        for i in range(length):
            if i == length - 1:
                mimetype_handlers[i].set_next(None)
            else:
                mimetype_handlers[i].set_next(mimetype_handlers[i + 1])

    def _get_mimetype_handler_with_name(self, name, mimetype_handlers):
        """
        gets a mimetype handler with the given name from input mimetype handlers list.

        if not available, it returns None.

        :param str name: mimetype handler name to get its instance.
        :param list[AbstractMIMETypeHandlerBase] mimetype_handlers: list of mimetype handlers.

        :raises DuplicatedMIMETypeHandlerError: duplicated mimetype handler error.

        :rtype: AbstractMIMETypeHandlerBase
        """

        result = [item for item in mimetype_handlers if item.get_name() == name]

        if result is None or len(result) <= 0:
            return None

        if len(result) > 1:
            raise DuplicatedMIMETypeHandlerError('There are multiple mimetype handlers with '
                                                 'name [{name}]. it could be due to a '
                                                 'bug in registering mimetype handlers.'
                                                 .format(name=name))
        if len(result) == 1:
            return result[0]

    def get_mimetype_handlers(self, **options):
        """
        gets all registered mimetype handlers.

        it could filter mimetype handlers for a specific type if provided.
        it only returns the first mimetype handlers for each type, because
        all mimetype handlers for a given type, are chained together.

        :keyword type accepted_type: specifies to get mimetype handlers which are
                                     registered for the accepted type. if not provided,
                                     all mimetype handlers will be returned.

        :rtype: list[AbstractMIMETypeHandlerBase]
        """

        accepted_type = options.get('accepted_type', None)

        if accepted_type is None:
            all_mimetype_handlers = []
            for handler_type in self._handlers:
                all_mimetype_handlers.append(self._handlers[handler_type][0])
            return all_mimetype_handlers
        else:
            mimetype_handlers_keys = [key for key in self._handlers
                                      if issubclass(accepted_type, key)]

            specific_mimetype_handlers = []
            for key in mimetype_handlers_keys:
                specific_mimetype_handlers.append(self._handlers[key][0])

            return specific_mimetype_handlers
