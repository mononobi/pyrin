# -*- coding: utf-8 -*-
"""
serializer manager module.
"""

from pyrin.converters.serializer import SerializerPackage
from pyrin.converters.serializer.interface import AbstractSerializerBase
from pyrin.core.structs import Context, Manager
from pyrin.core.globals import NULL
from pyrin.utils.custom_print import print_warning
from pyrin.converters.serializer.exceptions import InvalidSerializerTypeError, \
    DuplicatedSerializerError


class SerializerManager(Manager):
    """
    serializer manager class.
    """

    package_class = SerializerPackage

    def __init__(self):
        """
        initializes an instance of SerializerManager.
        """

        super().__init__()

        # a dictionary containing information of registered serializers.
        # example: dic(type accepted_type: AbstractSerializerBase instance)
        self._serializers = Context()

    def serialize(self, value, **options):
        """
        serializes the given value.

        returns serialized value on success or the
        same input value if serialization fails.

        all extra keyword arguments will be passed to underlying serializer.

        :param object value: value to be serialized.

        :keyword ResultSchema result_schema: result schema instance to be
                                             used to create computed columns.
                                             defaults to None if not provided.

        :returns: serialized object
        :rtype: dict | list[dict]
        """

        if value is None:
            return value

        serializers = self.get_serializers(type(value))
        for item in serializers:
            serialized_value = item.serialize(value, **options)
            if serialized_value is not NULL:
                return serialized_value

        return value

    def register_serializer(self, instance, **options):
        """
        registers a new serializer or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a serializer which is already registered.

        :param AbstractSerializerBase instance: serializer to be registered.
                                                it must be an instance of
                                                AbstractSerializerBase.

        :keyword bool replace: specifies that if there is another registered
                               serializer with the same accepted type,
                               replace it with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidSerializerTypeError: invalid serializer type error.
        :raises DuplicatedSerializerError: duplicated serializer error.
        """

        if not isinstance(instance, AbstractSerializerBase):
            raise InvalidSerializerTypeError('Input parameter [{instance}] is '
                                             'not an instance of [{base}].'
                                             .format(instance=instance,
                                                     base=AbstractSerializerBase))

        if instance.accepted_type in self._serializers:
            old_instance = self._serializers.get(instance.accepted_type)
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedSerializerError('There is another registered '
                                                'serializer [{old}] for accepted type '
                                                '[{accepted_type}] but "replace" option '
                                                'is not set, so serializer [{instance}] '
                                                'could not be registered.'
                                                .format(old=old_instance,
                                                        accepted_type=instance.accepted_type,
                                                        instance=instance))

            print_warning('Serializer [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._serializers[instance.accepted_type] = instance

    def get_serializers(self, accepted_type):
        """
        gets the registered serializers for given type.

        it returns an empty list if no serializer found for given type.

        :param type accepted_type: gets the serializers which are
                                   registered for the accepted type.

        :rtype: list[AbstractSerializerBase]
        """

        serializers = []
        if accepted_type in self._serializers:
            serializers.append(self._serializers.get(accepted_type))

        for key, instance in self._serializers.items():
            if key is not accepted_type and issubclass(accepted_type, key):
                serializers.append(instance)

        return serializers
