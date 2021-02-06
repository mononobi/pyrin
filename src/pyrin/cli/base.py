# -*- coding: utf-8 -*-
"""
cli base module.
"""

import subprocess

from subprocess import CalledProcessError
from threading import Lock
from abc import abstractmethod

from pyrin.cli.mixin.param import CLIParamMixin
from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.cli.exceptions import InvalidCLIHandlerNameError


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

    @abstractmethod
    def get_name(self):
        """
        gets current handler name, the handler will be registered with this name.

        the name must be the exact command name that this handler handles.
        for example `revision`.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def execute(self, **options):
        """
        executes the current cli command with given inputs.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: execution result.
        """

        raise CoreNotImplementedError()


class CLIHandlerBase(CLIParamMixin, AbstractCLIHandlerBase):
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

        :keyword bool help_param: specifies that help param must
                                  be added for this handler.
                                  defaults to True if not provided.

        :raises InvalidCLIHandlerNameError: invalid cli handler name error.
        """

        if name in (None, '') or name.isspace():
            raise InvalidCLIHandlerNameError('CLI handler name must be provided.')

        self._name = name
        super().__init__(**options)

    def __str__(self):
        """
        gets the string representation of current cli handler.

        :rtype: str
        """

        return '{base} [{handler}]'.format(base=super().__str__(), handler=self._name)

    def get_name(self):
        """
        gets current handler name, the handler will be registered with this name.

        the name must be the exact command name that this handler handles.
        for example `revision`.

        :rtype: str
        """

        return self._name

    def execute(self, **options):
        """
        executes the current cli command with given inputs.

        :rtype: int
        """

        return self._execute(**options)

    def _execute(self, **options):
        """
        executes the current cli command with given inputs.

        :rtype: int
        """

        commands = []
        self._inject_command_name(commands)
        processed_inputs = self._process_inputs(**options)
        self._bind_cli_arguments(commands, **processed_inputs)
        common_options = self._get_common_cli_options()
        common_options.extend(commands)
        return self._execute_on_cli(common_options)

    def _inject_command_name(self, commands):
        """
        injects the command name into given commands list.

        this method could be overridden in subclasses if a
        different behaviour is required.

        :param list commands: a list of all commands to inject
                              this command's name into it.
        """

        commands.insert(0, self.get_name())

    def _execute_on_cli(self, commands):
        """
        executes the current cli command with given inputs.

        :param list commands: a list of all commands and their
                              values to be sent to cli command.

        :rtype: int
        """

        try:
            result = subprocess.check_call(commands)
            return self._process_return_value(result)
        except CalledProcessError as error:
            return self._process_return_value(error.returncode)

    def _process_return_value(self, result):
        """
        processes the return value from cli command execution.

        this method returns the None value and is intended to be overridden
        by subclasses if required. if a cli handlers group does need to return
        a value, it could override this method and return the desired value.

        :param int result: result value returned from cli command.

        :rtype: object
        """

        return None

    def _get_common_cli_options(self):
        """
        gets the list of common cli options.

        this method is intended to be overridden by subclasses
        to inject some common cli options into the commands list.
        subclasses must return a list containing all common options.
        the common options will be inserted into beginning of the commands list.

        :rtype: list
        """

        return []
