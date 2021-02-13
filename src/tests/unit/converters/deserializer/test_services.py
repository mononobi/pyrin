# -*- coding: utf-8 -*-
"""
deserializer test_services module.
"""

import pytest

from sqlalchemy.pool import QueuePool, AssertionPool

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.handlers.base import DeserializerBase
from pyrin.core.structs import DTO
from pyrin.converters.deserializer.handlers.boolean import BooleanDeserializer
from pyrin.converters.deserializer.handlers.dictionary import DictionaryDeserializer
from pyrin.converters.deserializer.handlers.list import StringListDeserializer
from pyrin.converters.deserializer.exceptions import InvalidDeserializerTypeError, \
    DuplicatedDeserializerError


def test_deserialize_bool_from_string():
    """
    deserializes the given boolean value from string.
    """

    value = deserializer_services.deserialize('TruE')
    assert value is True

    value = deserializer_services.deserialize('false')
    assert value is False

    value = deserializer_services.deserialize(' FALSE ')
    assert value is False


def test_deserialize_datetime_from_string():
    """
    deserializes the given datetime value from string.
    note that all date times will be normalized into utc with 0 offset.
    """

    value = deserializer_services.deserialize('2019-09-01T20:12:15+00:30')

    # we have to check both halves of the year to prevent test failure
    # on different times of the year.
    assert (value.day == 1 and value.month == 9 and value.year == 2019 and
            value.second == 15 and value.minute == 12 and value.hour == 20) or \
           (value.day == 1 and value.month == 9 and value.year == 2019 and
            value.second == 15 and value.minute == 42 and value.hour == 19)


def test_deserialize_date_from_string():
    """
    deserializes the given date value from string.
    """

    value = deserializer_services.deserialize('2019-09-01')
    assert value.day == 1 and value.month == 9 and value.year == 2019


def test_deserialize_time_with_timezone_from_string():
    """
    deserializes the given time value which has timezone from string.
    """

    value = deserializer_services.deserialize('20:12:15+00:30')
    assert value.second == 15 and value.minute == 12 and value.hour == 20


def test_deserialize_time_without_timezone_from_string():
    """
    deserializes the given time value which has no timezone from string.
    """

    value = deserializer_services.deserialize('20:12:15')
    assert value.second == 15 and value.minute == 12 and value.hour == 20


def test_deserialize_string_from_string():
    """
    deserializes the given string value from string.
    it should not convert the value to it's real type
    because of the enclosing single or double quotes.
    """

    value = deserializer_services.deserialize('"nuLL"')
    assert value == 'nuLL'

    value = deserializer_services.deserialize("'123'")
    assert value == '123'

    value = deserializer_services.deserialize('"true"')
    assert value == 'true'


def test_deserialize_none_from_string():
    """
    deserializes the given none value from string.
    """

    value = deserializer_services.deserialize('nuLL')
    assert value is None

    value = deserializer_services.deserialize('none')
    assert value is None

    value = deserializer_services.deserialize(' NONE')
    assert value is None


def test_deserialize_int_from_string():
    """
    deserializes the given integer value from string.
    """

    value = deserializer_services.deserialize('1001')
    assert value == 1001

    value = deserializer_services.deserialize('-2032221')
    assert value == -2032221


def test_deserialize_float_from_string():
    """
    deserializes the given float value from string.
    """

    value = deserializer_services.deserialize('1.1001')
    assert value == 1.1001

    value = deserializer_services.deserialize('-2032.221')
    assert value == -2032.221

    value = deserializer_services.deserialize('00.02')
    assert value == '00.02'


def test_deserialize_pool_from_string():
    """
    deserializes the given pool class from string.
    """

    value = deserializer_services.deserialize('queuePOOL')
    assert issubclass(value, QueuePool)

    value = deserializer_services.deserialize('AssertionPool')
    assert issubclass(value, AssertionPool)


def test_deserialize_list_from_string():
    """
    deserializes the given list from string.
    """

    value = deserializer_services.deserialize('[ 1,   2,  3 ,   55 ]')
    assert value == [1, 2, 3, 55]


def test_deserialize_list_from_empty_string():
    """
    deserializes the given list from empty string.
    """

    value = deserializer_services.deserialize('[]')
    assert value is not None
    assert isinstance(value, list)
    assert len(value) == 0


def test_deserialize_tuple_from_string():
    """
    deserializes the given tuple from string.
    """

    value = deserializer_services.deserialize('( 22,   2,  3 ,   100 )')
    assert value == (22, 2, 3, 100)


def test_deserialize_tuple_from_empty_string():
    """
    deserializes the given tuple from empty string.
    """

    value = deserializer_services.deserialize('()')
    assert value is not None
    assert isinstance(value, tuple)
    assert len(value) == 0


def test_deserialize_dictionary_from_string():
    """
    deserializes the given dictionary from string.
    """

    dict_string = '{"bool_value": true, "datetime_value": "2000-10-20T12:10:43+00:00",' \
                  ' "date_value": "2004-11-01", "invalid_date_value": "2008-08-1",' \
                  ' "list_value": ["1", "False "], "list_string": "[ 1, -2.3, 0.01.1, null]",' \
                  ' "tuple_string": "(3, false ,-0)", "none_value": "none", ' \
                  ' "int_value": "1001 ", "float_value": " 2.4 ", "invalid_int": "1 2", ' \
                  ' "positive_float": " +405.0023", "pool_class": "assertionPool",' \
                  ' "single_string": "\'14\'"}'

    converted_values = deserializer_services.deserialize(dict_string)
    assert converted_values is not None
    assert isinstance(converted_values, dict)
    assert converted_values.get('bool_value') is True
    assert converted_values.get('invalid_date_value') == '2008-08-1'
    assert converted_values.get('list_value') == [1, False]
    assert converted_values.get('list_string') == [1, -2.3, '0.01.1', None]
    assert converted_values.get('tuple_string') == (3, False, '-0')
    assert converted_values.get('none_value') is None
    assert converted_values.get('int_value') == 1001
    assert converted_values.get('float_value') == 2.4
    assert converted_values.get('invalid_int') == '1 2'
    assert converted_values.get('positive_float') == ' +405.0023'
    assert converted_values.get('single_string') == '14'
    assert issubclass(converted_values.get('pool_class'), AssertionPool)

    datetime_value = converted_values.get('datetime_value')
    assert datetime_value.day == 20 and datetime_value.month == 10 and \
        datetime_value.year == 2000 and datetime_value.second == 43 and \
        datetime_value.minute == 10 and datetime_value.hour == 12

    date_value = converted_values.get('date_value')
    assert date_value.day == 1 and date_value.month == 11 and date_value.year == 2004


def test_deserialize_dictionary_from_empty_string():
    """
    deserializes the given dictionary from empty string.
    """

    dict_string = '{}'

    converted_value = deserializer_services.deserialize(dict_string)
    assert converted_value is not None
    assert isinstance(converted_value, dict)
    assert len(converted_value) == 0


def test_deserialize_list_items():
    """
    deserializes the given list items from list.
    """

    value = deserializer_services.deserialize(['1 ', ' True ', '-2', ' QueuePool'])
    assert value == [1, True, -2, QueuePool]


def test_deserialize_tuple_items():
    """
    deserializes the given tuple items from list.
    """

    value = deserializer_services.deserialize(('1 ', ' true', ' -2', ' QueuePool ', ' None'))
    assert value == (1, True, -2, QueuePool, None)


def test_deserialize_dictionary_items():
    """
    deserializes the given dictionary items from dictionary.
    """

    values = DTO(bool_value='true', datetime_value='2000-10-20T12:10:43+00:00',
                 date_value='2004-11-01', invalid_date_value='2008-08-1',
                 list_value=['1', 'False '], list_string='[ 1,  -2.3,  0.01.1,  null]',
                 tuple_value=(' 23', 'None', ' -78 '), tuple_string='(3,  false ,  -0)',
                 none_value='none', int_value='1001 ', float_value=' 2.4 ',
                 invalid_int='1 2', positive_float=' +405.0023', pool_class='assertionPool',
                 force_double_string='"123"', force_single_string="'true'")

    converted_values = deserializer_services.deserialize(values)
    assert converted_values is not None
    assert isinstance(converted_values, dict)
    assert converted_values.get('bool_value') is True
    assert converted_values.get('invalid_date_value') == '2008-08-1'
    assert converted_values.get('list_value') == [1, False]
    assert converted_values.get('list_string') == [1, -2.3, '0.01.1', None]
    assert converted_values.get('tuple_value') == (23, None, -78)
    assert converted_values.get('tuple_string') == (3, False, '-0')
    assert converted_values.get('none_value') is None
    assert converted_values.get('int_value') == 1001
    assert converted_values.get('float_value') == 2.4
    assert converted_values.get('invalid_int') == '1 2'
    assert converted_values.get('positive_float') == ' +405.0023'
    assert converted_values.get('force_double_string') == '123'
    assert converted_values.get('force_single_string') == 'true'
    assert issubclass(converted_values.get('pool_class'), AssertionPool)

    datetime_value = converted_values.get('datetime_value')
    assert datetime_value.day == 20 and datetime_value.month == 10 and \
        datetime_value.year == 2000 and datetime_value.second == 43 and \
        datetime_value.minute == 10 and datetime_value.hour == 12

    date_value = converted_values.get('date_value')
    assert date_value.day == 1 and date_value.month == 11 and date_value.year == 2004


def test_deserialize_failure():
    """
    tests values that should not be deserialized.
    it should return the same input and should raise error
    only on datetime value.
    """

    value = deserializer_services.deserialize('1 1')
    assert value == '1 1'

    value = deserializer_services.deserialize('trues')
    assert value == 'trues'

    with pytest.raises(ValueError):
        deserializer_services.deserialize('2018-13-21T10:11:23-00:30')

    value = deserializer_services.deserialize('[1, [2, 3], 5]')
    assert value == '[1, [2, 3], 5]'

    value = deserializer_services.deserialize('(1, (2, 3), 5)')
    assert value == '(1, (2, 3), 5)'

    value = deserializer_services.deserialize('non')
    assert value == 'non'

    value = deserializer_services.deserialize('1.23.4')
    assert value == '1.23.4'

    value = deserializer_services.deserialize('invalidPool')
    assert value == 'invalidPool'

    value = deserializer_services.deserialize('"mismatch_quoted''')
    assert value == '"mismatch_quoted'''

    value = deserializer_services.deserialize(None)
    assert value is None


def test_register_deserializer_invalid_type():
    """
    registers a new deserializer which has invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidDeserializerTypeError):
        deserializer_services.register_deserializer(DTO())


def test_register_deserializer_duplicate():
    """
    registers a duplicated deserializer which has been already registered.
    it should raise an error.
    """

    with pytest.raises(DuplicatedDeserializerError):
        deserializer_services.register_deserializer(BooleanDeserializer())


def test_register_deserializer_duplicate_with_replace():
    """
    registers a duplicated deserializer which has been already registered
    with replace option. it should not raise an error.
    """

    deserializer_services.register_deserializer(BooleanDeserializer(), replace=True)


def test_get_deserializers():
    """
    gets all registered deserializers.
    """

    values = deserializer_services.get_deserializers()
    assert len(values) == 4
    assert all(isinstance(item, DeserializerBase) for item in values)


def test_get_deserializers_string():
    """
    gets all registered deserializers for string accepted type.
    """

    values = deserializer_services.get_deserializers(accepted_type=str)
    assert len(values) == 1


def test_get_deserializers_tuple():
    """
    gets all registered deserializers for tuple accepted type.
    """

    values = deserializer_services.get_deserializers(accepted_type=tuple)
    assert len(values) == 1


def test_get_deserializers_list():
    """
    gets all registered deserializers for list accepted type.
    """

    values = deserializer_services.get_deserializers(accepted_type=list)
    assert len(values) == 1


def test_get_deserializers_dictionary():
    """
    gets all registered deserializers for list accepted type.
    """

    values = deserializer_services.get_deserializers(accepted_type=dict)
    assert len(values) == 1


def test_get_deserializers_not_supported_type():
    """
    gets all registered deserializers for not supported type.
    """

    values = deserializer_services.get_deserializers(accepted_type=int)
    assert len(values) == 0

    values = deserializer_services.get_deserializers(accepted_type=float)
    assert len(values) == 0

    values = deserializer_services.get_deserializers(accepted_type=bool)
    assert len(values) == 0


def test_deserializer_is_singleton():
    """
    tests that different types of deserializers are singleton.
    """

    deserializer1 = DictionaryDeserializer()
    deserializer2 = DictionaryDeserializer()

    assert deserializer1 == deserializer2

    values = deserializer_services.get_deserializers(accepted_type=dict)
    assert len(values) == 1
    assert values[0] == deserializer1
    assert values[0] == deserializer2

    deserializer3 = StringListDeserializer()
    deserializer4 = StringListDeserializer()

    assert deserializer3 == deserializer4
