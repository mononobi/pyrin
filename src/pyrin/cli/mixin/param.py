# -*- coding: utf-8 -*-
"""
cli mixin param module.
"""

from copy import deepcopy

from pyrin.cli.params import CLIParamBase, HelpParam
from pyrin.core.globals import LIST_TYPES
from pyrin.cli.arguments import PositionalArgument
from pyrin.core.structs import CoreObject
from pyrin.cli.exceptions import PositionalArgumentsIndicesError, InvalidCLIParamTypeError


class CLIParamMixin(CoreObject):
    """
    cli param mixin class.

    every cli handler class that needs to manage
    cli parameters must be subclassed from this.
    """

    def __init__(self, **options):
        """
        initializes an instance of CLIParamMixin.

        :keyword bool help_param: specifies that help param must
                                  be added for this handler.
                                  defaults to True if not provided.

        :raises PositionalArgumentsIndicesError: positional arguments indices error.
        """

        super().__init__()

        self._params = []
        help_param = options.get('help_param', True)
        params = self.__get_params(help_param)
        self._process_params(params)

    def _process_params(self, params):
        """
        processes the cli params that should be added.

        :param list[CLIParamBase] params: cli params of this handler.

        :raises InvalidCLIParamTypeError: invalid cli param type error.
        :raises PositionalArgumentsIndicesError: positional arguments indices error.
        """

        self.__extend_params(params)
        self._validate_positional_arguments()

    def _validate_positional_arguments(self):
        """
        validates the positional arguments.

        it will make sure that their indices are correct.

        :raises PositionalArgumentsIndicesError: positional arguments indices error.
        """

        positionals = [item for item in self._params
                       if isinstance(item, PositionalArgument)
                       and item.validate_index is not False]

        length = len(positionals)
        if length > 0:
            indices = [item.index for item in positionals]
            required_indices = list(range(0, length))

            if sorted(indices) != sorted(required_indices):
                raise PositionalArgumentsIndicesError('CLI handler [{handler}] has {length} '
                                                      'positional arguments {args}, but '
                                                      'indices of positional arguments are '
                                                      'incorrect. indices must be in the '
                                                      'range of {indices} for each argument '
                                                      'and it must be unique per argument. '
                                                      'the current indices are {current}.'
                                                      .format(handler=self,
                                                              length=length,
                                                              args=positionals,
                                                              indices=required_indices,
                                                              current=indices))

    def __add_param(self, item):
        """
        adds the given item into params list.

        :param CLIParamBase item: cli param to be added.

        :raises InvalidCLIParamTypeError: invalid cli param type error.
        """

        if not isinstance(item, CLIParamBase):
            raise InvalidCLIParamTypeError('Input parameter [{param}] is not '
                                           'an instance of [{instance}].'
                                           .format(param=item,
                                                   instance=CLIParamBase))

        self._params.append(item)

    def __extend_params(self, items):
        """
        extends params list with the given items.

        :param list[CLIParamBase] items: cli params to be added.

        :raises InvalidCLIParamTypeError: invalid cli param type error.
        """

        for item in items:
            self.__add_param(item)

    def _process_inputs(self, **options):
        """
        processes the inputs in given dict with all available params.

        :rtype: dict
        """

        processed_inputs = deepcopy(options)
        for item in self._params:
            processed_inputs = item.process_inputs(**processed_inputs)

        return processed_inputs

    def _bind_cli_arguments(self, commands, **options):
        """
        binds cli arguments with values available in options.

        it adds items into the exact input list.
        options are a mapping of real python method inputs.

        :param list[object] commands: cli commands list.

        :returns: list of all commands in the form of:
                  [str name1, str value1, ...] or
                  [str name1, str value1, str value2, ...]

        :rtype: list
        """

        start = len(commands)
        for param in self._params:
            real_value = options.get(param.param_name, None)
            representation = param.get_representation(real_value)

            if representation is None:
                continue

            if isinstance(param, PositionalArgument):
                if isinstance(representation, LIST_TYPES):
                    self._inject_positional_arguments(commands, representation,
                                                      param.index + start)
                else:
                    commands.insert(param.index + start, representation)
            elif isinstance(representation, LIST_TYPES):
                commands.extend(representation)
            else:
                commands.append(representation)

    def _inject_positional_arguments(self, commands, arguments, index):
        """
        injects (in-place) given arguments into specified index of given commands list.

        :param list[object] commands: list of cli commands.

        :param list[object] arguments: arguments that must be
                                       injected into commands list.

        :param index: zero-based index in which arguments must be injected.
        """

        for item_index, item in enumerate(arguments):
            commands.insert(index + item_index, item)

    def __get_params(self, help_param=True):
        """
        gets the list of current handler's prams.

        :param bool help_param: specifies that help param
                                must also be added to params list.
                                defaults to True if not provided.

        :rtype: list[CLIParamBase]
        """

        params = []
        if help_param is True:
            params.append(HelpParam())

        self._inject_params(params)
        return params

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        all subclasses that want to override this method to inject
        their params into the given list must call `super()._inject_params(params)`
        after their work has been done.

        :param list[CLIParamBase] params: list of all params.
        """
        pass
