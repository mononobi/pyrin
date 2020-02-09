# -*- coding: utf-8 -*-
"""
cli interface module.
"""

import subprocess

from subprocess import CalledProcessError
from threading import Lock

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.globals import LIST_TYPES
from pyrin.utils.singleton import MultiSingletonMeta
from pyrin.cli.exceptions import MetaDataOptionsParamNameIsRequiredError, \
    ParamValueIsNotMappedToCLIError, InvalidCLIHandlerNameError


class CLIHandlerSingletonMeta(MultiSingletonMeta):
    """
    cli handler singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractCLIHandlerBase(CoreObject, metaclass=CLIHandlerSingletonMeta):
    """
    abstract cli handler base class.
    """

    def get_name(self):
        """
        gets this handlers name, the handler will be registered with this name.
        the name must be the exact command name that this handler handles.
        for example `revision`.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def execute(self, **options):
        """
        executes the current cli command with given inputs.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: execution result.
        """

        raise CoreNotImplementedError()


class CLIHandlerOptionsMetadata(CoreObject):
    """
    cli handler options metadata class.
    """

    def __init__(self, param_name,
                 cli_option_name=None,
                 param_value_to_cli_map=None,
                 default=None):
        """
        initializes an instance of CLIHandlerOptionsMetadata.

        :param str param_name: param name presented in method signature.

        :param Union[str, None] cli_option_name: relevant cli option name to `param_name`.
                                                 it could be None if command does
                                                 not have a name for this argument.
                                                 for example the `--autogenerate` flag
                                                 of alembic, could be present to imply to
                                                 `True` and absent to imply to `False`.
                                                 but `--message` flag of alembic must be
                                                 present with the message value itself.

        :param Union[dict, None] param_value_to_cli_map: a dictionary containing a mapping
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
                                                         but `--message` flag of alembic does
                                                         not have a mapping, so its dict must
                                                         be empty and instead the
                                                         `cli_option_name` must be set to
                                                         `--message` and then the exact value
                                                         of method parameter will be emitted
                                                         as the value of this flag.

        :param Union[str, None] default: default value to be emitted to cli if this
                                         param is not available. if set to None, this
                                         param will not be emitted at all.

        :raises MetaDataOptionsParamNameIsRequiredError: cli handler metadata
                                                         options param name
                                                         is required error.
        """

        super().__init__()

        if param_name in (None, '') or param_name.isspace():
            raise MetaDataOptionsParamNameIsRequiredError('CLI handler options '
                                                          'metadata "param_name" '
                                                          'must be provided.')

        self.param_name = param_name
        self.cli_option_name = cli_option_name
        self.default = default

        if param_value_to_cli_map is not None and len(param_value_to_cli_map) > 0:
            self.param_value_to_cli_map = param_value_to_cli_map
        else:
            self.param_value_to_cli_map = None


class CLIHandlerBase(AbstractCLIHandlerBase):
    """
    cli handler base class.
    all application cli handlers must be subclassed from this.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of CLIHandlerBase.

        :param str name: the handler name that should be registered
                         with. this name must be the exact name that
                         this handler must emmit to cli.
        """

        super().__init__()

        if name in (None, '') or name.isspace():
            raise InvalidCLIHandlerNameError('CLI handler name must be provided.')

        self._name = name
        self._options_meta_data = self._generate_cli_handler_options_metadata()

    def get_name(self):
        """
        gets this handlers name, the handler will be registered with this name.
        the name must be the exact command name that this handler handles.
        for example `revision`.

        :rtype: str
        """

        return self._name

    def _generate_cli_handler_options_metadata(self):
        """
        generates cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        result = []
        common = self._generate_common_cli_handler_options_metadata()
        custom = self._generate_custom_cli_handler_options_metadata()
        result.extend(common)
        result.extend(custom)

        return result

    def _generate_common_cli_handler_options_metadata(self):
        """
        generates common cli handler options metadata.
        this method is intended to be overridden by
        base handler for each category. if the handlers does not have
        any common options, you could leave this method unimplemented.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        return []

    def _generate_custom_cli_handler_options_metadata(self):
        """
        generates custom cli handler options metadata.
        this method is intended to be overridden
        by each concrete handler.
        if the handler does not accept any options, you
        could leave this method unimplemented.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        return []

    def execute(self, **options):
        """
        executes the current cli command with given inputs.

        :returns: execution result.
        """

        return self._execute(**options)

    def _execute(self, **options):
        """
        executes the current cli command with given inputs.

        :returns: execution result.
        """

        bounded_options = self._bind_cli_options(**options)
        self._inject_common_cli_options(bounded_options)
        return self._execute_on_cli(bounded_options)

    def _execute_on_cli(self, commands):
        """
        executes the current cli command with given inputs.

        :param list commands: a list of all commands and their
                              values to be sent to cli command.

        :returns: execution result.
        """

        try:
            return subprocess.check_call(commands)
        except CalledProcessError:
            pass

    def _inject_common_cli_options(self, commands):
        """
        this method is intended to be used by subclasses
        to inject some common cli options into the given list.
        subclasses must add some items into the given list if required.

        :param list commands: a list of all commands and their
                              values to be sent to cli.
        """
        pass

    def _bind_cli_options(self, **options):
        """
        binds cli options of current handler with values available in options.
        options are a mapping of real python method inputs.

        :returns: list of all command in the form of
                  [str name1, str value1, ...] or [str name2, ...]

        :raises ParamValueIsNotMappedToCLIError: param value is not mapped to cli error.

        :rtype: list
        """

        commands = [self.get_name()]
        for metadata in self._options_meta_data:
            real_value = options.get(metadata.param_name, None)

            if metadata.cli_option_name not in (None, '') and not \
                    metadata.cli_option_name.isspace() and \
                    self._should_send_to_cli(real_value, metadata.default) is True:
                commands.append(metadata.cli_option_name)

            if metadata.param_value_to_cli_map is not None:
                if real_value is not None and \
                        real_value not in metadata.param_value_to_cli_map:
                    raise ParamValueIsNotMappedToCLIError('Parameter value [{value}] '
                                                          'for parameter with name [{name}] '
                                                          'is not present in cli map, if '
                                                          'you want to always pass this '
                                                          'parameters real value to cli, you '
                                                          'must not provide any key arguments '
                                                          'into "param_value_to_cli_map" '
                                                          'input of "CLIHandlerOptionsMetadata" '
                                                          'class constructor. and also if you '
                                                          'want to not pass this argument to '
                                                          'cli on specific values, you must '
                                                          'provide those values as keys of '
                                                          '"param_value_to_cli_map" input of '
                                                          '"CLIHandlerOptionsMetadata" class '
                                                          'constructor with `None` value '
                                                          'attached to those keys.'
                                                          .format(value=real_value,
                                                                  name=metadata.param_name))

                cli_value = metadata.param_value_to_cli_map.get(real_value, metadata.default)
                if cli_value is not None:
                    commands.append(cli_value)
            elif self._should_send_to_cli(real_value, metadata.default):
                if real_value is None:
                    real_value = metadata.default

                if isinstance(real_value, LIST_TYPES):
                    real_value = ' '.join([str(item) for item in real_value])
                commands.append(real_value)

        return commands

    def _should_send_to_cli(self, real_value, default_value):
        """
        gets a value indicating that this param should be sent to cli.

        :param object real_value: real value of method param.
        :param str default_value: default value of options metadata.

        :rtype: bool
        """

        return real_value is not None or default_value is not None
