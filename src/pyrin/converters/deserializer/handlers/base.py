# -*- coding: utf-8 -*-
"""
deserializer handlers base module.
"""

from abc import abstractmethod

from pyrin.converters.deserializer.exceptions import InvalidDeserializerTypeError
from pyrin.converters.deserializer.interface import AbstractDeserializerBase
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.globals import NULL
from pyrin.utils.string import remove_line_break_escapes


class DeserializerBase(AbstractDeserializerBase):
    """
    deserializer base class.
    """

    def __init__(self, **options):
        """
        initializes an instance of DeserializerBase.
        """

        super().__init__()
        self._next_handler = None

    def deserialize(self, value, **options):
        """
        deserializes the given value.

        returns `NULL` object if deserialization fails.

        :param object value: value to be deserialized.

        :returns: deserialized value.
        """

        deserialized_value = self._deserialize_operation(value, **options)
        if deserialized_value is NULL:
            if self._next_handler is not None:
                return self._next_handler.deserialize(value, **options)

        if isinstance(deserialized_value, str):
            deserialized_value = remove_line_break_escapes(deserialized_value)

        return deserialized_value

    def _deserialize_operation(self, value, **options):
        """
        deserializes the given value.

        it checks if the value is deserializable, if so, deserializes it.
        otherwise returns `NULL` object.
        this method could be overridden in other base subclasses if required.

        :param object value: value to be deserialized.

        :returns: deserialized value.
        """

        deserialized_value = NULL
        if self.is_deserializable(value, **options) is True:
            deserialized_value = self._deserialize(value, **options)

        return deserialized_value

    @abstractmethod
    def _deserialize(self, value, **options):
        """
        deserializes the given value.

        returns `NULL` object if deserialization fails.
        this method is intended to be overridden in subclasses.

        :param object value: value to be deserialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: deserialized value.
        """

        raise CoreNotImplementedError()

    def set_next(self, deserializer):
        """
        sets the next deserializer handler and returns it.

        :param DeserializerBase deserializer: deserializer instance to
                                              be set as next handler.

        :rtype: DeserializerBase
        """

        if deserializer is not None and not isinstance(deserializer, DeserializerBase):
            raise InvalidDeserializerTypeError('Input parameter [{instance}] is not '
                                               'an instance of [{base}].'
                                               .format(instance=deserializer,
                                                       base=DeserializerBase))

        self._next_handler = deserializer
        return deserializer

    def is_deserializable(self, value, **options):
        """
        gets a value indicating that the given input is deserializable.

        :param object value: value to be deserialized.

        :rtype: bool
        """

        return isinstance(value, self.accepted_type)


class StringDeserializerBase(DeserializerBase):
    """
    string deserializer base class.
    """

    # these values will be used for accepted
    # formats that have no length restriction.
    UNDEF_LENGTH = None
    DEFAULT_MIN = 1
    DEFAULT_MAX = 1000000

    def __init__(self, **options):
        """
        initializes an instance of StringDeserializerBase.

        :keyword list[tuple[str, int]] accepted_formats: custom formats and their length
                                                         that this deserializer can
                                                         deserialize value from.

        :note accepted_formats: list[tuple[str format, int length]]
        """

        super().__init__(**options)

        self._accepted_formats = self.default_formats
        custom_accepted_formats = options.get('accepted_formats', [])
        self._accepted_formats.extend(custom_accepted_formats)

        # min and max accepted length of strings
        # to be deserialized by this deserializer.
        self._min_length, self._max_length = self._calculate_accepted_length()

    def is_deserializable(self, value, **options):
        """
        gets a value indicating that the given input is deserializable.

        :param object value: value to be deserialized.

        :rtype: bool
        """

        if super().is_deserializable(value, **options) \
                and self.is_valid_length(value.strip()):
            return True

        return False

    @property
    def accepted_type(self):
        """
        gets the accepted type for this deserializer.

        which could deserialize values from this type.

        :rtype: type[str]
        """

        return str

    @property
    def accepted_length(self):
        """
        gets the min and max accepted length of strings to be deserialized.

        :returns: tuple[int min, int max]
        :rtype: tuple[int, int]
        """

        return self._min_length, self._max_length

    @property
    def accepted_formats(self):
        """
        gets the accepted string formats that this deserializer can deserialize value from.

        :returns: list[tuple[str format, int length]]
        :rtype: list[tuple[str, int]]
        """

        return self._accepted_formats

    def is_valid_length(self, value):
        """
        gets a value indicating that input value has valid length to be deserialized.

        :param str value: value to be deserialized.

        :rtype: bool
        """

        length = len(value.strip())
        min_length, max_length = self.accepted_length

        if length < min_length or length > max_length:
            return False

        return True

    def _calculate_accepted_length(self):
        """
        calculates the min and max accepted length of values to be deserialized.

        :returns: tuple[int min, int max]
        :rtype: tuple[int, int]
        """

        # if there is any format with length=UNDEF_LENGTH,
        # we should not enforce length restriction on values.
        if self.UNDEF_LENGTH in [item[1] for item in self.accepted_formats]:
            return self.DEFAULT_MIN, self.DEFAULT_MAX

        return min([item[1] for item in self.accepted_formats]), \
            max([item[1] for item in self.accepted_formats])

    @property
    @abstractmethod
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: list[tuple[str format, int length]]
        :rtype: list[tuple[str, int]]
        """

        raise CoreNotImplementedError()


class StringPatternDeserializerBase(StringDeserializerBase):
    """
    string pattern deserializer base class.

    this class uses regex to determine whether a value is deserializable or not.
    """

    def __init__(self, **options):
        """
        initializes an instance of StringPatternDeserializerBase.

        :keyword list[tuple[Pattern, int]] accepted_formats: custom patterns and their length
                                                             that this deserializer can
                                                             deserialize value from.

        :note accepted_formats: list[tuple[Pattern format, int length]]
        """

        super().__init__(**options)

    def is_deserializable(self, value, **options):
        """
        gets a value indicating that the given input is deserializable.

        if the value is deserializable, the matching `Pattern` would also be returned.
        otherwise None would be returned instead of `Pattern`.

        :param object value: value to be deserialized.

        :rtype: tuple[bool, Pattern]
        """

        if super().is_deserializable(value, **options):
            pattern = self.get_matching_pattern(value.strip())
            if pattern is not None:
                return True, pattern

        return False, None

    def _deserialize_operation(self, value, **options):
        """
        deserializes the given value.

        it checks if the value is deserializable, if so, deserializes it.
        otherwise returns `NULL` object.
        if the value is deserializable, the matching `Pattern` would also
        be injected into options with `matching_pattern` key to be used in
        `_deserialize()` method implementation.
        it's better to pop `matching_pattern` in `_deserialize()` method
        for usage instead of get.

        :param object value: value to be deserialized.

        :returns: deserialized value.
        """

        deserialized_value = NULL
        deserializable, pattern = self.is_deserializable(value, **options)
        if deserializable is True:
            options.update(matching_pattern=pattern)
            deserialized_value = self._deserialize(value.strip(), **options)

        return deserialized_value

    def get_matching_pattern(self, value):
        """
        gets the matching pattern for given value. returns None if no pattern found.

        :param object value: value to be deserialized.

        :rtype: Pattern
        """

        for pattern, length in self.accepted_formats:
            if pattern.match(value):
                return pattern

        return None
