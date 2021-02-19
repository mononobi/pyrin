# -*- coding: utf-8 -*-
"""
string normalizer manager module.
"""

from collections import OrderedDict

import pyrin.utils.dictionary as dict_utils

from pyrin.core.structs import Context, Manager
from pyrin.utilities.string.normalizer import StringNormalizerPackage
from pyrin.utilities.string.normalizer.enumerations import NormalizerEnum
from pyrin.utilities.string.normalizer.exceptions import StringNormalizerDoesNotExistError
from pyrin.utilities.string.normalizer.interface import AbstractStringNormalizerBase
from pyrin.utils.custom_print import print_warning
from pyrin.utilities.string.normalizer.exceptions import InvalidStringNormalizerTypeError, \
    DuplicatedStringNormalizerError


class StringNormalizerManager(Manager):
    """
    string normalizer manager class.
    """

    package_class = StringNormalizerPackage

    def __init__(self):
        """
        initializes an instance of StringNormalizerManager.
        """

        super().__init__()

        # a dictionary containing information of registered normalizers.
        # example: dict(str name: AbstractStringNormalizerBase instance)
        self._normalizers = Context()

        # a dictionary containing name of normalizers and their priority.
        # values are ordered from max to min priority.
        # example: dict(str name: int priority)
        self._priorities = OrderedDict()

    def normalize(self, value, *normalizers, **options):
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

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :raises StringNormalizerDoesNotExistError: string normalizer does not exist error.

        :returns: normalized value.
        :rtype: str
        """

        normalize_none = options.get('normalize_none', False)
        if value is None and normalize_none is True:
            value = ''

        if value in (None, ''):
            return value

        if normalizers is None or len(normalizers) <= 0:
            normalizers = self._priorities.keys()

        for name in normalizers:
            normalizer = self.get_normalizer(name)
            value = normalizer.normalize(value, **options)

            if value == '':
                break

        return value

    def register_normalizer(self, instance, **options):
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

        if not isinstance(instance, AbstractStringNormalizerBase):
            raise InvalidStringNormalizerTypeError('Input parameter [{instance}] is '
                                                   'not an instance of [{base}].'
                                                   .format(instance=instance,
                                                           base=AbstractStringNormalizerBase))

        if instance.get_name() in self._normalizers:
            old_instance = self._normalizers.get(instance.get_name())
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedStringNormalizerError('There is another registered '
                                                      'string normalizer with name [{name}] '
                                                      'but "replace" option is not set, so '
                                                      'normalizer [{instance}] could not '
                                                      'be registered.'
                                                      .format(name=instance.get_name(),
                                                              instance=instance))

            print_warning('String normalizer [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._normalizers[instance.get_name()] = instance
        self._priorities[instance.get_name()] = instance.priority
        self._priorities = OrderedDict(dict_utils.sort_by_value(self._priorities,
                                                                reverse=True))

    def get_normalizer(self, name, **options):
        """
        gets the string normalizer with given name.

        it raises an error if normalizer does not exist.

        :raises StringNormalizerDoesNotExistError: string normalizer does not exist error.

        :rtype: AbstractStringNormalizerBase
        """

        if name in self._normalizers:
            return self._normalizers.get(name)

        raise StringNormalizerDoesNotExistError('String normalizer with name [{name}] '
                                                'does not exist.'.format(name=name))

    def space(self, value, **options):
        """
        remove all spaces from the string.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.SPACE)
        return normalizer.normalize(value, **options)

    def duplicate_space(self, value, **options):
        """
        replace all duplicate spaces with a single one.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.DUPLICATE_SPACE)
        return normalizer.normalize(value, **options)

    def lowercase(self, value, **options):
        """
        lowercase the string.

        :param str value: value to be lower-cased.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.LOWERCASE)
        return normalizer.normalize(value, **options)

    def uppercase(self, value, **options):
        """
        uppercase the string.

        :param str value: value to be upper-cased.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.UPPERCASE)
        return normalizer.normalize(value, **options)

    def title_case(self, value, **options):
        """
        title case the string.

        :param str value: value to be title-cased.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.TITLE_CASE)
        return normalizer.normalize(value, **options)

    def filter(self, value, **options):
        """
        remove filters from the string.

        :param str value: value to be filtered.

        :keyword list[str] filters: list of items to be removed from value.

        :keyword bool ignore_case: remove `filters` from string in case-insensitive
                                   way. defaults to True if not provided.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.FILTER)
        return normalizer.normalize(value, **options)

    def persian_sign(self, value, **options):
        """
        remove common persian signs from the string.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.PERSIAN_SIGN)
        return normalizer.normalize(value, **options)

    def latin_sign(self, value, **options):
        """
        remove common latin signs from the string.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.LATIN_SIGN)
        return normalizer.normalize(value, **options)

    def persian_number(self, value, **options):
        """
        replace persian numbers with latin numbers.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.PERSIAN_NUMBER)
        return normalizer.normalize(value, **options)

    def arabic_number(self, value, **options):
        """
        replace arabic numbers with latin numbers.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.ARABIC_NUMBER)
        return normalizer.normalize(value, **options)

    def persian_letter(self, value, **options):
        """
        normalize persian letters.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.PERSIAN_LETTER)
        return normalizer.normalize(value, **options)

    def latin_letter(self, value, **options):
        """
        normalize latin letters.

        :param str value: value to be normalized.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :rtype: str
        """

        normalizer = self.get_normalizer(NormalizerEnum.LATIN_LETTER)
        return normalizer.normalize(value, **options)
