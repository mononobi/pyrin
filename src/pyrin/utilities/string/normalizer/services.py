# -*- coding: utf-8 -*-
"""
string normalizer services module.
"""

from pyrin.utilities.string.normalizer import StringNormalizerPackage
from pyrin.application.services import get_component


def normalize(value, *normalizers, **options):
    """
    normalizes the given value.

    :param str value: value to be normalized.

    :param str normalizers: normalizer names to be used.
                            they will be used in the order of their appearance.
                            if not provided, all normalizers will be used with
                            the order of their priority attribute.

    :keyword list[str] filters: list of items to be removed from string.
                                defaults to None. it will only be used
                                for `filter` normalizer.

    :keyword bool ignore_case: remove `filters` from string in case-insensitive
                               way. defaults to True if not provided.

    :keyword bool strip: strip spaces from both ends of string on each
                         normalization step. defaults to True if not provided.

    :raises StringNormalizerDoesNotExistError: string normalizer does not exist error.

    :returns: normalized value.
    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).normalize(value,
                                                                           *normalizers,
                                                                           **options)


def register_normalizer(instance, **options):
    """
    registers a new string normalizer or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a normalizer which is already registered.

    :param AbstractStringNormalizerBase instance: normalizer to be registered.
                                                  it must be an instance of
                                                  AbstractStringNormalizerBase.

    :keyword bool replace: specifies that if there is another registered
                           normalizer with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidStringNormalizerTypeError: invalid string normalizer type error.
    :raises DuplicatedStringNormalizerError: duplicated string normalizer error.
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).register_normalizer(instance,
                                                                                     **options)


def get_normalizer(name, **options):
    """
    gets the string normalizer with given name.

    it raises an error if normalizer does not exist.

    :raises StringNormalizerDoesNotExistError: string normalizer does not exist error.

    :rtype: AbstractStringNormalizerBase
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).get_normalizer(name, **options)


def space(value, **options):
    """
    remove all spaces from the string.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).space(value, **options)


def duplicate_space(value, **options):
    """
    replace all duplicate spaces with a single one.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).duplicate_space(value,
                                                                                 **options)


def lowercase(value, **options):
    """
    lowercase the string.

    :param str value: value to be lower-cased.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).lowercase(value, **options)


def uppercase(value, **options):
    """
    uppercase the string.

    :param str value: value to be upper-cased.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).uppercase(value, **options)


def title_case(value, **options):
    """
    title case the string.

    :param str value: value to be title-cased.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).title_case(value, **options)


def filter(value, **options):
    """
    remove filters from the string.

    :param str value: value to be filtered.

    :keyword list[str] filters: list of items to be removed from value.

    :keyword bool ignore_case: remove `filters` from string in case-insensitive
                               way. defaults to True if not provided.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).filter(value, **options)


def persian_sign(value, **options):
    """
    remove common persian signs from the string.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).persian_sign(value, **options)


def latin_sign(value, **options):
    """
    remove common latin signs from the string.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).latin_sign(value, **options)


def persian_number(value, **options):
    """
    replace persian numbers with latin numbers.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).persian_number(value, **options)


def arabic_number(value, **options):
    """
    replace arabic numbers with latin numbers.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).arabic_number(value, **options)


def persian_letter(value, **options):
    """
    normalize persian letters.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).persian_letter(value, **options)


def latin_letter(value, **options):
    """
    normalize latin letters.

    :param str value: value to be normalized.

    :rtype: str
    """

    return get_component(StringNormalizerPackage.COMPONENT_NAME).latin_letter(value, **options)
