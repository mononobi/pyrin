# -*- coding: utf-8 -*-
"""
cli metadata module.
"""

from pyrin.core.globals import LIST_TYPES
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.context import CoreObject, DTO
from pyrin.cli.exceptions import ArgumentMetadataParamNameIsRequiredError, \
    PositionalArgumentMetadataIndexError, BooleanArgumentMetadataValueError, \
    KeywordArgumentMetadataCLIOptionNameError, \
    MappingArgumentMetadataParamValueToCLIMapRequiredError, \
    KeywordArgumentMetadataCLIOptionNameRequiredError


class ArgumentMetadataBase(CoreObject):
    """
    argument metadata base class.
    """

    def __init__(self, param_name, default=None):
        """
        initializes an instance of ArgumentMetadataBase.

        :param str param_name: param name presented in method signature.

        :param Union[object, None] default: default value to be emitted to cli if this
                                            param is not available. if set to None, this
                                            param will not be emitted at all.
                                            defaults to None if not provided.

        :raises ArgumentMetadataParamNameIsRequiredError: argument metadata param
                                                          name is required error.
        """

        super().__init__()

        if param_name in (None, '') or param_name.isspace():
            raise ArgumentMetadataParamNameIsRequiredError('Argument metadata '
                                                           '"param_name" '
                                                           'must be provided.')
        self._param_name = param_name

        if isinstance(default, LIST_TYPES):
            default = self._prepare_list_type(default)

        self._default = default

    def get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param object value: value of method input that should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this metadata. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: Union[list[object], object, None]
        """

        if isinstance(value, LIST_TYPES):
            value = self._prepare_list_type(value)

        result = self._get_representation(value, is_default)
        if result is None and is_default is False:
            return self.get_representation(self._default, True)

        return result

    @property
    def default(self):
        """
        gets the default value of this argument metadata.

        :rtype: Union[object, None]
        """

        return self._default

    @property
    def param_name(self):
        """
        gets the param name of this argument metadata.

        :rtype: str
        """

        return self._param_name

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.
        this method is intended to be overridden in subclasses.

        :param object value: value of method input that should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this metadata. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: Union[list[object], object, None]
        """

        raise CoreNotImplementedError()

    def _prepare_list_type(self, value):
        """
        prepares list type value for cli representation.

        actually, it converts any object of list, set or
        tuple type into a space separated string.
        this is needed because command line only could
        handle arrays this way.

        if there is any requirement for subclasses to return an
        actual list, they can override this method and return
        the actual list.

        :param Union[list, set, tuple] value: array value to be converted.

        :returns: space separated string of all items.
        :rtype: str
        """

        result = ' '.join([str(item) for item in value])
        return result


class KeywordArgumentMetadataBase(ArgumentMetadataBase):
    """
    keyword argument metadata base class.
    """

    def __init__(self, param_name, cli_option_name=None, default=None):
        """
        initializes an instance of KeywordArgumentMetadataBase.

        :param str param_name: param name presented in method signature.

        :param Union[str, None] cli_option_name: relevant cli option name to `param_name`.
                                                 for example `--message` flag of alembic
                                                 must be present with the message value
                                                 itself. defaults to None if not provided.

        :param Union[object, None] default: default value to be emitted to cli if this
                                            param is not available. if set to None, this
                                            param will not be emitted at all.
                                            defaults to None if not provided.

        :raises ArgumentMetadataParamNameIsRequiredError: argument metadata param
                                                          name is required error.

        :raises KeywordArgumentMetadataCLIOptionNameError: keyword argument metadata
                                                           cli option name error.
        """

        super().__init__(param_name, default)

        if cli_option_name is not None and \
                (cli_option_name.isspace() or cli_option_name == ''):
            raise KeywordArgumentMetadataCLIOptionNameError('Keyword argument metadata '
                                                            '"cli_option_name" could '
                                                            'be None or have a valid '
                                                            'value. blank is not valid.')

        self._cli_option_name = cli_option_name

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param object value: value of method input that should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this metadata. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: Union[list[object], object, None]
        """

        return self._merge_inputs(value)

    def _merge_inputs(self, value):
        """
        merges the cli option name and given value to be emitted to cli.

        :param Union[list[object], object, None] value: value to be emitted to cli.

        :rtype: Union[list[object], object, None]
        """

        if value is None:
            return None

        if self._cli_option_name is not None:
            result = [self._cli_option_name]
            if isinstance(value, LIST_TYPES):
                result.extend(value)
            else:
                result.append(value)
            return result

        return value


class PositionalArgumentMetadata(ArgumentMetadataBase):
    """
    positional argument metadata class.

    this class must be used for positional cli arguments.
    """

    def __init__(self, param_name, index, default=None):
        """
        initializes an instance of PositionalArgumentMetadata.

        :param str param_name: param name presented in method signature.
        :param int index: zero based index of this param in cli command inputs.

        :param Union[object, None] default: default value to be emitted to cli if this
                                            param is not available. if set to None, this
                                            param will not be emitted at all.
                                            defaults to None if not provided.

        :raises ArgumentMetadataParamNameIsRequiredError: argument metadata param
                                                          name is required error.

        :raises PositionalArgumentMetadataIndexError: positional argument
                                                      metadata index error.
        """

        super().__init__(param_name, default)

        if index is None or index < 0:
            raise PositionalArgumentMetadataIndexError('Positional argument metadata '
                                                       '"index" could not be less than zero.')
        self._index = index

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param object value: value of method input that should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this metadata. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: Union[object, None]
        """

        return value

    @property
    def index(self):
        """
        gets the index in which this param must be emitted to cli command.

        :rtype: int
        """

        return self._index


class MappingArgumentMetadata(KeywordArgumentMetadataBase):
    """
    mapping argument metadata class.

    this class must be used for cli options that have mappings.
    """

    def __init__(self, param_name, param_value_to_cli_map,
                 cli_option_name=None, default=None):
        """
        initializes an instance of MappingArgumentMetadata.

        :param str param_name: param name presented in method signature.

        :param dict param_value_to_cli_map: a dictionary containing a mapping
                                            between different method param values
                                            and their representation on cli. for
                                            example the `--autogenerate` flag of
                                            alembic, could be present to imply to
                                            `True` and absent to imply to `False`.
                                            so this dict should contain two keys,
                                            one is `True` and its value must be
                                            '--autogenerate' and another is `False`
                                            with the `None` value to prevent
                                            emitting to cli.

        :param Union[str, None] cli_option_name: relevant cli option name to `param_name`.
                                                 it could be None if command does
                                                 not have a name for this argument.
                                                 for example the `--autogenerate` flag
                                                 of alembic, could be present to imply to
                                                 `True` and absent to imply to `False`.
                                                 but `--message` flag of alembic must
                                                 always be provided with given message.
                                                 defaults to None if not provided.

        :param Union[object, None] default: default value to be emitted to cli if this
                                            param is not available. if set to None, this
                                            param will not be emitted at all.
                                            defaults to None if not provided.

        :raises ArgumentMetadataParamNameIsRequiredError: argument metadata param
                                                          name is required error.

        :raises KeywordArgumentMetadataCLIOptionNameError: keyword argument metadata
                                                           cli option name error.

        :raises MappingArgumentMetadataParamValueToCLIMapRequiredError: mapping argument
                                                                        metadata param value
                                                                        to cli map required
                                                                        error.
        """

        super().__init__(param_name, cli_option_name, default)

        if param_value_to_cli_map is None or len(param_value_to_cli_map) <= 0:
            raise MappingArgumentMetadataParamValueToCLIMapRequiredError(
                'Mapping argument metadata "param_value_to_cli_map" '
                'is required. it should contain at least one key/value.'
            )

        self._param_value_to_cli_map = self._normalize_list_types(param_value_to_cli_map)

    def _normalize_list_types(self, value):
        """
        normalizes all list type objects in given dict values and returns a new dict.

        actually, it converts any object of list, set or
        tuple type into a space separated string.
        this is needed because command line only could
        handle arrays this way.

        if there is any requirement for subclasses to use an
        actual list, they can override this method and return
        the exact same input value.

        :param dict value: dictionary to normalize all list type values of it.

        :rtype: dict
        """

        result = DTO()
        for key, item in value.items():
            if isinstance(item, LIST_TYPES):
                result[key] = self._prepare_list_type(item)
            else:
                result[key] = item

        return result

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param object value: value of method input that should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this metadata. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: Union[list[object], object, None]
        """

        if is_default is False:
            value = self._param_value_to_cli_map.get(value, None)

        return super()._get_representation(value, is_default)


class BooleanArgumentMetadata(MappingArgumentMetadata):
    """
    boolean argument metadata class.

    this class must be used for boolean cli arguments.
    """

    def __init__(self, param_name, true_value,
                 false_value=None, default=None):
        """
        initializes an instance of BooleanArgumentMetadata.

        :param str param_name: param name presented in method signature.

        :param object true_value: the value that should be emitted to cli for True.

        :param Union[object, None] false_value: the value that should be emitted to cli
                                                for False. if not provided, defaults to
                                                None and will not be emitted.

        :param Union[object, None] default: default value to be emitted to cli if this
                                            param is not available. if set to None, this
                                            param will not be emitted at all.
                                            defaults to None if not provided.

        :raises ArgumentMetadataParamNameIsRequiredError: argument metadata param
                                                          name is required error.

        :raises BooleanArgumentMetadataValueError: boolean argument metadata value error.
        """

        if true_value is None and false_value is None:
            raise BooleanArgumentMetadataValueError('Boolean argument metadata "true_value" '
                                                    'or "false_value" must be provided.')
        self._true_value = true_value
        self._false_value = false_value

        mapping = DTO()
        mapping[True] = true_value
        mapping[False] = false_value

        super().__init__(param_name, mapping, None, default)


class KeywordArgumentMetadata(KeywordArgumentMetadataBase):
    """
    keyword argument metadata class.

    it should be used for keyword argument cli options.
    """

    def __init__(self, param_name, cli_option_name, default=None):
        """
        initializes an instance of KeywordArgumentMetadata.

        :param str param_name: param name presented in method signature.

        :param str cli_option_name: relevant cli option name to `param_name`.
                                    for example `--message` flag of alembic
                                    must be present with the message value itself.

        :param Union[object, None] default: default value to be emitted to cli if this
                                            param is not available. if set to None, this
                                            param will not be emitted at all.
                                            defaults to None if not provided.

        :raises ArgumentMetadataParamNameIsRequiredError: argument metadata param
                                                          name is required error.

        :raises KeywordArgumentMetadataCLIOptionNameRequiredError: keyword argument metadata
                                                                   cli option name required
                                                                   error.
        """

        if cli_option_name in (None, '') or cli_option_name.isspace():
            raise KeywordArgumentMetadataCLIOptionNameRequiredError('Keyword argument metadata '
                                                                    '"cli_option_name" '
                                                                    'must be provided.')
        super().__init__(param_name, cli_option_name, default)
