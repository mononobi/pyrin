# -*- coding: utf-8 -*-
"""
cli arguments module.
"""

from abc import ABC, abstractmethod

from flask import json as flask_json

from pyrin.core.globals import LIST_TYPES
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject, DTO
from pyrin.cli.exceptions import ArgumentParamNameIsRequiredError, \
    PositionalArgumentIndexError, BooleanArgumentValueError, \
    KeywordArgumentCLIOptionNameError, MappingArgumentParamValueToCLIMapRequiredError, \
    KeywordArgumentCLIOptionNameRequiredError


class ArgumentBase(CoreObject, ABC):
    """
    argument base class.
    """

    def __init__(self, param_name, default=None):
        """
        initializes an instance of ArgumentBase.

        :param str param_name: param name presented in method signature.

        :param list[object] | object default: default value to be emitted to
                                              cli if this param is not available.
                                              if set to None, this param will not
                                              be emitted at all.
                                              defaults to None if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.
        """

        super().__init__()

        if param_name in (None, '') or param_name.isspace():
            raise ArgumentParamNameIsRequiredError('Argument "param_name" '
                                                   'must be provided.')
        self._param_name = param_name
        self._default = default

    def __str__(self):
        """
        gets the string representation of current argument.

        :rtype: str
        """

        return '{base} [{param}]'.format(base=super().__str__(), param=self.param_name)

    def _convert_result(self, value):
        """
        converts the given value to required type.

        this method is intended to be overridden in subclasses if they
        need the result to be of a specific type.

        :param list[object] | object value: value to be converted.

        :rtype: list[object] | object
        """

        return value

    def get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param list[object] | object value: value of method input
                                            that should be represented
                                            in cli.

        :param bool is_default: specifies that input value is the default
                                value of this argument. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: list[object] | object
        """

        if isinstance(value, (set, tuple)):
            value = list(value)

        result = self._get_representation(value, is_default)

        if result is None and is_default is False:
            return self.get_representation(self._default, True)

        return self._convert_result(result)

    @property
    def default(self):
        """
        gets the default value of this argument.

        :rtype: list[object] | object
        """

        return self._default

    @property
    def param_name(self):
        """
        gets the param name of this argument.

        :rtype: str
        """

        return self._param_name

    @abstractmethod
    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param list[object] | object value: value of method input that
                                            should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this argument. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: list[object] | object
        """

        raise CoreNotImplementedError()


class KeywordArgumentBase(ArgumentBase):
    """
    keyword argument base class.
    """

    def __init__(self, param_name, cli_option_name=None, default=None):
        """
        initializes an instance of KeywordArgumentBase.

        :param str param_name: param name presented in method signature.

        :param str cli_option_name: relevant cli option name to `param_name`.
                                    for example `--message` flag of alembic
                                    must be present with the message value
                                    itself. defaults to None if not provided.

        :param list[object] | object default: default value to be emitted to
                                              cli if this param is not available.
                                              if set to None, this param will not
                                              be emitted at all.
                                              defaults to None if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.
        :raises KeywordArgumentCLIOptionNameError: keyword argument cli option name error.
        """

        super().__init__(param_name, default)

        if cli_option_name is not None and \
                (cli_option_name.isspace() or cli_option_name == ''):
            raise KeywordArgumentCLIOptionNameError('Keyword argument "cli_option_name" '
                                                    'could be None or have a valid '
                                                    'value. blank is not valid.')

        self._cli_option_name = cli_option_name

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param list[object] | object value: value of method input that
                                            should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this argument. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: list[object] | object
        """

        return self._merge_inputs(value)

    def _merge_inputs(self, value):
        """
        merges the cli option name and given value to be emitted to cli.

        note that the values of list type, must be emitted separately
        using the `cli_option_name`. for example if value = [1, 2, 3]
        and `cli_option_name` is `--num`, then it should be emitted to
        cli like this: ['--num', 1, '--num', 2, '--num', 3]
        if the cli handler supports multiple values with single name
        (for example pybabel commands), you should use
        `CompositeKeywordArgument` class instead.

        :param list[object] | object value: value to be emitted to cli.

        :rtype: list[object] | object
        """

        if value is None:
            return None

        if self._cli_option_name is not None:
            result = []
            if isinstance(value, LIST_TYPES):
                for item in value:
                    result.extend([self._cli_option_name, item])
            else:
                result.extend([self._cli_option_name, value])
            return result

        return value


class PositionalArgument(ArgumentBase):
    """
    positional argument class.

    this class must be used for positional cli arguments.
    positional arguments are those that will be emitted after
    command name at specified index and without any argument
    name, for example: `command value1`
    """

    def __init__(self, param_name, index, default=None, **options):
        """
        initializes an instance of PositionalArgument.

        :param str param_name: param name presented in method signature.
        :param int index: zero based index of this param in cli command inputs.

        :param list[object] | object default: default value to be emitted to
                                              cli if this param is not available.
                                              if set to None, this param will not
                                              be emitted at all.
                                              defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.

        :raises PositionalArgumentIndexError: positional argument index error.
        """

        super().__init__(param_name, default)

        if index is None or index < 0:
            raise PositionalArgumentIndexError('Positional argument "index" '
                                               'could not be less than zero.')
        self._index = index
        self._validate_index = options.get('validate_index', True)

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param list[object] | object value: value of method input that
                                            should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this argument. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: list[object] | object
        """

        return value

    @property
    def index(self):
        """
        gets the index in which this param must be emitted to cli command.

        :rtype: int
        """

        return self._index

    @property
    def validate_index(self):
        """
        gets a value indicating that index of this argument must be validated.

        :rtype: bool
        """

        return self._validate_index


class CompositePositionalArgument(PositionalArgument):
    """
    composite positional argument class.

    this class must be used for composite positional cli arguments.
    composite positional arguments are those that will be emitted after
    command name at specified index and without any argument name, and the
    value could be a list.
    for example: `command value1` or `command value1 value2 value3`
    """

    def __init__(self, param_name, index, default=None,
                 separator=None, **options):
        """
        initializes an instance of CompositePositionalArgument.

        :param str param_name: param name presented in method signature.
        :param int index: zero based index of this param in cli command inputs.

        :param list[object] | object default: default value to be emitted to
                                              cli if this param is not available.
                                              if set to None, this param will not
                                              be emitted at all.
                                              defaults to None if not provided.

        :param str separator: separator to be used between values of list type.
                              defaults to single space if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.

        :raises PositionalArgumentIndexError: positional argument index error.
        """

        super().__init__(param_name, index, default, **options)

        if separator is None:
            separator = ' '

        self._separator = separator

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param list[object] | object value: value of method input that
                                            should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this argument. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: str
        """

        if value is None:
            return None

        result = value
        if isinstance(value, LIST_TYPES):
            result = self._separator.join([str(item) for item in value])

        return super()._get_representation(result, is_default)


class MappingArgument(KeywordArgumentBase):
    """
    mapping argument class.

    this class must be used for cli options that have mappings.
    these are arguments that their real value that should be emitted
    to cli, will be extracted from a dict based on the input of the
    python-side method. they could have argument name or could be emitted
    without any argument name.
    usually you don't need to use an instance of this class directly.
    """

    def __init__(self, param_name, param_value_to_cli_map,
                 cli_option_name=None, default=None):
        """
        initializes an instance of MappingArgument.

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

        :param str cli_option_name: relevant cli option name to `param_name`.
                                    it could be None if command does
                                    not have a name for this argument.
                                    for example the `--autogenerate` flag
                                    of alembic, could be present to imply to
                                    `True` and absent to imply to `False`.
                                    but `--message` flag of alembic must
                                    always be provided with given message.
                                    defaults to None if not provided.

        :param list[object] | object default: default value to be emitted to
                                              cli if this param is not available.
                                              if set to None, this param will not
                                              be emitted at all.
                                              defaults to None if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.

        :raises KeywordArgumentCLIOptionNameError: keyword argument cli option name error.

        :raises MappingArgumentParamValueToCLIMapRequiredError: mapping argument param value
                                                                to cli map required error.
        """

        super().__init__(param_name, cli_option_name, default)

        if param_value_to_cli_map is None or len(param_value_to_cli_map) <= 0:
            raise MappingArgumentParamValueToCLIMapRequiredError(
                'Mapping argument "param_value_to_cli_map" is '
                'required. it should contain at least one key/value.'
            )

        self._param_value_to_cli_map = param_value_to_cli_map

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param list[object] | object value: value of method input that
                                            should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this argument. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: list[object] | object
        """

        if is_default is False and value is not None:
            value = self._param_value_to_cli_map.get(value)

        return super()._get_representation(value, is_default)


class BooleanArgument(MappingArgument):
    """
    boolean argument class.

    this class must be used for boolean cli arguments.
    boolean arguments are those that will emit a keyword to imply to True
    and will not emit anything to imply to False. for example:
    `command --arg1` -> the value of `arg1` will be True in this form.
    `command` -> in this form the value of `arg1` will be False.
    """

    def __init__(self, param_name, true_value,
                 false_value=None, default=None):
        """
        initializes an instance of BooleanArgument.

        :param str param_name: param name presented in method signature.

        :param object true_value: the value that should be emitted to cli for True.

        :param object false_value: the value that should be emitted to cli
                                   for False. if not provided, defaults to
                                   None and will not be emitted.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.

        :raises BooleanArgumentValueError: boolean argument value error.
        """

        if true_value is None and false_value is None:
            raise BooleanArgumentValueError('Boolean argument "true_value" or '
                                            '"false_value" must be provided.')
        self._true_value = true_value
        self._false_value = false_value

        mapping = DTO()
        mapping[True] = true_value
        mapping[False] = false_value

        super().__init__(param_name, mapping, None, default)

    def _get_representation(self, value, is_default=False):
        """
        gets the representation of current cli option based on given input.

        it could be None if the value should not be emitted to cli.

        :param list[object] | object value: value of method input that
                                            should be represented in cli.

        :param bool is_default: specifies that input value is the default
                                value of this argument. it might be needed
                                for some subclasses to differentiate between
                                default value and other values.
                                defaults to False if not provided.

        :rtype: list[object] | object
        """

        if is_default is True and value is not None:
            value = value is True
            is_default = False

        return super()._get_representation(value, is_default)


class KeywordArgument(KeywordArgumentBase):
    """
    keyword argument class.

    it should be used for keyword argument cli options.
    keyword arguments are those that have to emit an argument name
    with an argument value, note that this type of arguments could not
    emit a list for a single argument. instead, if the value for a single
    argument is a list, each item in the list will be emitted separately
    with `--arg` name. for example:
    `command --arg1 value1` -> for single value.
    `command --arg1 item1 --arg1 item2 --arg1 item3` -> for a list value.
    if the cli handler supports keyword arguments with list values, you should
    use `CompositeKeywordArgument` class.
    """

    def __init__(self, param_name, cli_option_name, default=None):
        """
        initializes an instance of KeywordArgument.

        :param str param_name: param name presented in method signature.

        :param str cli_option_name: relevant cli option name to `param_name`.
                                    for example `--message` flag of alembic
                                    must be present with the message value itself.

        :param list[object] | object default: default value to be emitted to
                                              cli if this param is not available.
                                              if set to None, this param will not
                                              be emitted at all.
                                              defaults to None if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.

        :raises KeywordArgumentCLIOptionNameRequiredError: keyword argument cli option
                                                           name required error.
        """

        if cli_option_name in (None, '') or cli_option_name.isspace():
            raise KeywordArgumentCLIOptionNameRequiredError('Keyword argument '
                                                            '"cli_option_name" '
                                                            'must be provided.')

        super().__init__(param_name, cli_option_name, default)


class CompositeKeywordArgument(KeywordArgument):
    """
    composite keyword argument class.

    it should be used for composite keyword argument cli options.
    composite keyword arguments are those that have to emit an argument
    name with an argument value, note that this type of arguments could
    emit a list for a single argument with `--arg` name. for example:
    `command --arg1 value1` -> for single value.
    `command --arg1 item1 item2 item3` -> for a list value.
    if the cli handler does not support keyword arguments with list
    values, you should use `KeywordArgument` class.
    """

    def __init__(self, param_name, cli_option_name, separator=None, default=None):
        """
        initializes an instance of CompositeKeywordArgument.

        :param str param_name: param name presented in method signature.

        :param str cli_option_name: relevant cli option name to `param_name`.
                                    for example `--message` flag of alembic
                                    must be present with the message value itself.

        :param str separator: separator to be used between values of list type.
                              defaults to single space if not provided.

        :param list[object] | object default: default value to be emitted to
                                              cli if this param is not available.
                                              if set to None, this param will not
                                              be emitted at all.
                                              defaults to None if not provided.

        :raises ArgumentParamNameIsRequiredError: argument param name is required error.

        :raises KeywordArgumentCLIOptionNameRequiredError: keyword argument cli
                                                           option name required error.
        """

        super().__init__(param_name, cli_option_name, default)

        if separator is None:
            separator = ' '

        self._separator = separator

    def _merge_inputs(self, value):
        """
        merges the cli option name and given value to be emitted to cli.

        note that the values of list type, must be emitted using single
        `cli_option_name` separated with optional separator or space.
        for example if value = [1, 2, 3] and `cli_option_name` is `--num`
        and separator is `-` then it should be emitted to cli like this:
        ['--num', '1-2-3'] and if separator is None, then it should be
        emitted like this: ['--num', '1 2 3']
        if the cli handler does not support multiple values with single
        name (for example alembic commands), you should use
        `KeywordArgument` class instead.

        :param list[object] | object value: value to be emitted to cli.

        :rtype: list[object]
        """

        if value is None:
            return None

        result = [self._cli_option_name]
        if isinstance(value, LIST_TYPES):
            value = self._separator.join([str(item) for item in value])

        result.append(value)
        return result


class JSONKeywordArgument(KeywordArgument):
    """
    json keyword argument class.

    it should be used for json keyword argument cli options.
    json keyword arguments are those that have to emit an argument
    name with an argument value, note that this type of arguments must
    be emitted as a list or dict json string representation. for example:
    `command --arg1 '[value1, value2]'` -> for list value.
    `command --arg1 '{"key1": item1, "key2": item2}'` -> for a dict value.
    """

    def _merge_inputs(self, value):
        """
        merges the cli option name and given value to be emitted to cli.

        :param list[object] | dict[object] value: value to be emitted to cli.

        :rtype: list[object]
        """

        if value is None:
            return None

        if isinstance(value, (tuple, set)):
            value = list(value)

        result = [self._cli_option_name]
        value = flask_json.dumps(value)
        result.append(value)
        return result
