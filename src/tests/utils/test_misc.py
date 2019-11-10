# -*- coding: utf-8 -*-
"""
utils test_misc module.
"""

import pytest

import pyrin.utils.misc as misc_utils

from pyrin.core.context import DTO, CoreObject
from pyrin.core.exceptions import CoreAttributeError


def test_set_attributes():
    """
    sets the provided keyword arguments as attributes in given object instance.
    """

    instance = CoreObject()
    attributes = DTO(name='fake_name', age=23, is_valid=True)
    instance = misc_utils.set_attributes(instance, **attributes)

    assert instance is not None
    assert hasattr(instance, 'name') is True
    assert hasattr(instance, 'age') is True
    assert hasattr(instance, 'is_valid') is True

    assert getattr(instance, 'name') == 'fake_name'
    assert getattr(instance, 'age') == 23
    assert getattr(instance, 'is_valid') is True


def test_set_attributes_with_no_attributes():
    """
    sets the provided keyword arguments which is empty as attributes in
    given object instance. it should return the same inputted object.
    """

    instance = CoreObject()
    count = len(vars(instance).keys())
    attributes = DTO()
    instance = misc_utils.set_attributes(instance, **attributes)

    assert instance is not None
    assert len(vars(instance).keys()) == count


def test_set_attributes_with_none_instance():
    """
    sets the provided keyword arguments as attributes in given
    object instance which is None. it should return a None object.
    """

    instance = None
    attributes = DTO(name='fake_name', age=23, is_valid=True)
    instance = misc_utils.set_attributes(instance, **attributes)

    assert instance is None


def test_extract_attributes():
    """
    extracts all attributes with given names from provided object instance.
    """

    instance = CoreObject()
    attributes = DTO(name='fake_name', age=23, is_valid=True)
    instance = misc_utils.set_attributes(instance, **attributes)
    extracted_attrs = misc_utils.extract_attributes(instance, *attributes.keys())

    assert extracted_attrs is not None
    assert len(extracted_attrs.keys()) == 3
    assert extracted_attrs.get('name') == 'fake_name'
    assert extracted_attrs.get('age') == 23
    assert extracted_attrs.get('is_valid') is True


def test_extract_attributes_with_no_attributes():
    """
    extracts all attributes with given names which is
    empty from provided object instance. it should return an empty dict.
    """

    instance = CoreObject()
    attributes = DTO(name='fake_name', age=23, is_valid=True)
    instance = misc_utils.set_attributes(instance, **attributes)
    extracted_attrs = misc_utils.extract_attributes(instance, *[])

    assert extracted_attrs is not None
    assert len(extracted_attrs.keys()) == 0


def test_extract_attributes_with_none_instance():
    """
    extracts all attributes with given names from provided object
    instance which is None. it should return an empty dict.
    """

    instance = None
    attributes = DTO(name='fake_name', age=23, is_valid=True)
    extracted_attrs = misc_utils.extract_attributes(instance, *attributes.keys())

    assert extracted_attrs is not None
    assert len(extracted_attrs.keys()) == 0


def test_extract_attributes_with_unavailable_attributes():
    """
    extracts all attributes with given names from provided object instance.
    some of attributes are unavailable in object instance.
    it should raise an error.
    """

    with pytest.raises(CoreAttributeError):
        instance = CoreObject()
        attributes = DTO(name='fake_name', age=23, is_valid=True)
        instance = misc_utils.set_attributes(instance, **attributes)
        extracted_attrs = misc_utils.extract_attributes(instance, *['name', 'age',
                                                                    'is_valid',
                                                                    'extra_attr'])
