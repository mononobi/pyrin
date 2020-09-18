# -*- coding: utf-8 -*-
"""
cli mixin handler module.
"""

from pyrin.cli.base import CLIHandlerBase
from pyrin.core.structs import CoreObject, DTO
from pyrin.utils.custom_print import print_warning
from pyrin.cli.exceptions import InvalidCLIHandlerTypeError, DuplicatedCLIHandlerError, \
    CLIHandlerNotFoundError


class CLIMixin(CoreObject):
    """
    cli mixin class.

    every class that needs to manage cli handlers must inherit from this.
    """

    _cli_handler_type = CLIHandlerBase

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CLIMixin.
        """

        super().__init__()

        # a dictionary containing cli handlers for different commands.
        # in the form of: {str handler_name: CLIHandlerBase handler}
        self._cli_handlers = DTO()

    def register_cli_handler(self, instance, **options):
        """
        registers a new cli handler or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a cli handler which is already registered.

        :param CLIHandlerBase instance: cli handler to be registered.
                                        it must be an instance of CLIHandlerBase.

        :keyword bool replace: specifies that if there is another registered
                               cli handler with the same name, replace it
                               with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidCLIHandlerTypeError: invalid cli handler type error.
        :raises DuplicatedCLIHandlerError: duplicated cli handler error.
        """

        if not isinstance(instance, self._cli_handler_type):
            raise InvalidCLIHandlerTypeError('Input parameter [{instance}] is '
                                             'not an instance of [{handler}].'
                                             .format(instance=instance,
                                                     handler=self._cli_handler_type))

        if instance.get_name() in self._cli_handlers:
            old_instance = self._cli_handlers.get(instance.get_name())
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedCLIHandlerError('There is another registered '
                                                'cli handler with name [{name}] '
                                                'but "replace" option is not set, so '
                                                'cli handler [{instance}] could not '
                                                'be registered.'
                                                .format(name=instance.get_name(),
                                                        instance=instance))

            print_warning('CLI handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._cli_handlers[instance.get_name()] = instance

    def _get_cli_handler(self, name):
        """
        gets a cli handler with the given name.

        if not available, it raises an error.

        :param str name: cli handler name to get its instance.

        :raises CLIHandlerNotFoundError: cli handler not found error.

        :rtype: CLIHandlerBase
        """

        if name not in self._cli_handlers:
            raise CLIHandlerNotFoundError('CLI handler [{name}] not found.'
                                          .format(name=name))

        return self._cli_handlers[name]

    def execute(self, handler_name, **options):
        """
        executes the handler with the given name with given inputs.

        :param str handler_name: handler name to be executed.

        :raises CLIHandlerNotFoundError: cli handler not found error.

        :rtype: int
        """

        handler = self._get_cli_handler(handler_name)
        return handler.execute(**options)
