# -*- coding: utf-8 -*-
"""
deserializer manager module.
"""

from pyrin.converters.deserializer.exceptions import InvalidDeserializerTypeError, \
    DuplicatedDeserializerError
from pyrin.converters.deserializer.handlers.base import DeserializerBase
from pyrin.context import CoreObject, Context
from pyrin.utils.custom_print import print_warning


class DeserializerManager(CoreObject):
    """
    deserializer manager class.
    """

    def __init__(self):
        """
        initializes and instance of DeserializerManager.
        """

        CoreObject.__init__(self)

        # a dictionary containing information of registered deserializers.
        # example: dic(tuple(class_name, type): instance)
        self._deserializers = Context()

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

        :param object value: value to be deserialized.

        :rtype: object
        """

        options.update(accepted_type=type(value))
        deserialized_value = None

        for deserializer in self.get_deserializers(**options):
            deserialized_value = deserializer.deserialize(value, **options)

            if deserialized_value is not None:
                return deserialized_value
            continue

        return deserialized_value

    def register_deserializer(self, instance, **options):
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

        :raises InvalidDeserializerTypeError: invalid deserializer type error.
        :raises DuplicatedDeserializerError: duplicated deserializer error.
        """

        if not isinstance(instance, DeserializerBase):
            raise InvalidDeserializerTypeError('Input parameter [{instance}] is '
                                               'not an instance of DeserializerBase.'
                                               .format(instance=str(instance)))

        # checking whether is there any registered instance
        # with the same name and accepted type.
        if (instance.get_name(), instance.get_accepted_type()) in self._deserializers.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicatedDeserializerError('There is another registered deserializer '
                                                  'with name [{name}] and accepted type '
                                                  '[{accepted_type}] but "replace" option is '
                                                  'not set, so deserializer [{instance}] '
                                                  'could not be registered.'
                                                  .format(name=instance.get_name(),
                                                          accepted_type=
                                                          instance.get_accepted_type(),
                                                          instance=str(instance)))

            old_instance = self._deserializers[(instance.get_name(), instance.get_accepted_type())]
            print_warning('Deserializer [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(instance)))

        # registering new deserializer.
        self._deserializers[(instance.get_name(), instance.get_accepted_type())] = instance

    def get_deserializers(self, **options):
        """
        gets all registered deserializers.
        it could filter deserializers for a specific type if provided.

        :keyword type accepted_type: specifies to get deserializers which are registered for the
                                     accepted type. if not provided, all deserializers
                                     will be returned.

        :rtype: list[DeserializerBase]
        """

        accepted_type = options.get('accepted_type', None)

        # getting all deserializers.
        if accepted_type is None:
            return [value for value in self._deserializers.values()]

        # getting deserializers for given type.
        deserializer_keys = [key for key in self._deserializers.keys()
                             if issubclass(accepted_type, key[1])]
        return [self._deserializers[key] for key in deserializer_keys]
