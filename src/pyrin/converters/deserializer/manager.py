# -*- coding: utf-8 -*-
"""
deserializer manager module.
"""

from pyrin.converters.deserializer import DeserializerPackage
from pyrin.converters.deserializer.interface import AbstractDeserializerBase
from pyrin.core.structs import Context, Manager
from pyrin.core.globals import NULL
from pyrin.utils.custom_print import print_warning
from pyrin.converters.deserializer.exceptions import InvalidDeserializerTypeError, \
    DuplicatedDeserializerError


class DeserializerManager(Manager):
    """
    deserializer manager class.
    """

    package_class = DeserializerPackage

    def __init__(self):
        """
        initializes an instance of DeserializerManager.
        """

        super().__init__()

        # a dictionary containing information of registered deserializers.
        # example: dict(type accepted_type: list[AbstractDeserializerBase] instances)
        self._deserializers = Context()

    def deserialize(self, value, **options):
        """
        deserializes the given value.

        returns deserialized object on success or returns
        the same input value if deserialization fails.

        :param object value: value to be deserialized.

        :keyword bool include_internal: specifies that any chained internal deserializer
                                        must also be used for deserialization. if set to
                                        False, only non-internal deserializers will be used.
                                        defaults to True if not provided.

        :returns: deserialized object
        """

        options.update(accepted_type=type(value))
        for deserializer in self.get_deserializers(**options):
            deserialized_value = deserializer.deserialize(value, **options)

            if deserialized_value is not NULL:
                return deserialized_value
            continue

        return value

    def register_deserializer(self, instance, **options):
        """
        registers a new deserializer or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a deserializer which is already registered.

        :param AbstractDeserializerBase instance: deserializer to be registered.
                                                  it must be an instance of
                                                  AbstractDeserializerBase.

        :keyword bool replace: specifies that if there is another registered
                               deserializer with the same name and accepted type,
                               replace it with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidDeserializerTypeError: invalid deserializer type error.
        :raises DuplicatedDeserializerError: duplicated deserializer error.
        """

        if not isinstance(instance, AbstractDeserializerBase):
            raise InvalidDeserializerTypeError('Input parameter [{instance}] is '
                                               'not an instance of [{base}].'
                                               .format(instance=instance,
                                                       base=AbstractDeserializerBase))

        previous_instances = self._deserializers.get(instance.accepted_type, [])
        if instance.accepted_type in self._deserializers:
            if len(previous_instances) > 0:
                old_instance = self._get_deserializer_with_name(instance.get_name(),
                                                                previous_instances)
                if old_instance is not None:
                    replace = options.get('replace', False)
                    if replace is not True:
                        raise DuplicatedDeserializerError('There is another registered '
                                                          'deserializer with name [{name}] '
                                                          'for accepted type [{accepted_type}] '
                                                          'but "replace" option is not set, so '
                                                          'deserializer [{instance}] could not '
                                                          'be registered.'
                                                          .format(name=instance.get_name(),
                                                                  accepted_type=instance.
                                                                  accepted_type,
                                                                  instance=instance))

                    print_warning('Deserializer [{old_instance}] is going '
                                  'to be replaced by [{new_instance}].'
                                  .format(old_instance=old_instance,
                                          new_instance=instance))

                    previous_instances.remove(old_instance)

        previous_instances.append(instance)
        self._set_next_handlers(previous_instances)
        self._deserializers[instance.accepted_type] = previous_instances

    def _set_next_handlers(self, deserializers):
        """
        sets next handler for each deserializer in the input list.

        :param list[AbstractDeserializerBase] deserializers: list of deserializers.
        """

        length = len(deserializers)
        for i in range(length):
            if i == length - 1:
                deserializers[i].set_next(None)
            else:
                deserializers[i].set_next(deserializers[i + 1])

    def _get_deserializer_with_name(self, name, deserializers):
        """
        gets a deserializer with the given name from input deserializers list.

        if not available, it returns None.

        :param str name: deserializer name to get its instance.
        :param list[AbstractDeserializerBase] deserializers: list of deserializers.

        :raises DuplicatedDeserializerError: duplicated deserializer error.

        :rtype: AbstractDeserializerBase
        """

        result = [item for item in deserializers if item.get_name() == name]

        if result is None or len(result) <= 0:
            return None

        if len(result) > 1:
            raise DuplicatedDeserializerError('There are multiple deserializers with '
                                              'name [{name}]. it could be due to a '
                                              'bug in registering deserializers.'
                                              .format(name=name))
        if len(result) == 1:
            return result[0]

    def get_deserializers(self, **options):
        """
        gets all registered deserializers.

        it could filter deserializers for a specific type if provided.
        it only returns the first deserializer for each type, because
        all deserializers for a given type, are chained together.

        :keyword type accepted_type: specifies to get deserializers which are registered for
                                     the accepted type. if not provided, all deserializers
                                     will be returned.

        :rtype: list[AbstractDeserializerBase]
        """

        accepted_type = options.get('accepted_type', None)

        if accepted_type is None:
            all_deserializers = []
            for deserializer_type in self._deserializers:
                all_deserializers.append(self._deserializers[deserializer_type][0])
            return all_deserializers
        else:
            deserializer_keys = [key for key in self._deserializers
                                 if issubclass(accepted_type, key)]

            specific_deserializers = []
            for key in deserializer_keys:
                specific_deserializers.append(self._deserializers[key][0])

            return specific_deserializers
