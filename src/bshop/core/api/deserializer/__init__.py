# -*- coding: utf-8 -*-
"""
deserializer package.
"""

from bshop.core.api.deserializer.handlers.base import DeserializerBase
from bshop.core.context import Context
from bshop.core.exceptions import CoreTypeError, CoreKeyError

__deserializers__ = Context()


def _register_deserializer(instance, **options):
    """
    registers a new deserializer or replaces the existing one
    if `replace=True` is provided. otherwise, it raises an error
    on adding an instance which it's name and accepted type is already available
    in registered deserializers.

    :param DeserializerBase instance: deserializer to be registered.
                                      it must be an instance of DeserializerBase.

    :keyword bool replace: specifies that if there is another registered
                           deserializer with the same name and accepted type,
                           replace it with the new one, otherwise raise
                           an error. defaults to False.

    :raises CoreTypeError: core type error.
    :raises CoreKeyError: core key error.
    """

    global __deserializers__

    if not isinstance(instance, DeserializerBase):
        raise CoreTypeError('Input parameter [{instance}] is '
                            'not an instance of DeserializerBase.'
                            .format(instance=str(instance)))

    # checking whether is there any registered instance
    # with the same name and accepted type.
    if (instance.get_name(), instance.accepted_type()) in __deserializers__.keys():
        replace = options.get('replace', False)

        if not replace:
            raise CoreKeyError('There is another registered deserializer with name [{name}] '
                               'and accepted type [{accepted_type}] and "replace" option is not set, '
                               'so deserializer [{instance}] could not be registered.'
                               .format(name=instance.get_name(),
                                       accepted_type=instance.accepted_type(),
                                       instance=str(instance)))

        old_instance = __deserializers__[(instance.get_name(), instance.accepted_type())]
        print('Deserializer [{old_instance}] is going to be replaced by [{new_instance}].'
              .format(old_instance=str(old_instance), new_instance=str(instance)))

    __deserializers__[(instance.get_name(), instance.accepted_type())] = instance


def _get_deserializers(**options):
    """
    gets all registered deserializers.
    it could filter deserializers for a specific type if provided.

    :keyword type accepted_type: specifies to get deserializers which are registered for the
                                 accepted type. if not provided, all deserializers will be returned.

    :rtype: list[DeserializerBase]
    """

    accepted_type = options.get('accepted_type', None)

    if accepted_type is None:
        return [value for value in __deserializers__.values()]

    # getting all deserializer that are registered for the given type.
    deserializer_keys = [key for key in __deserializers__.keys() if issubclass(accepted_type, key[1])]
    return [__deserializers__[key] for key in deserializer_keys]
