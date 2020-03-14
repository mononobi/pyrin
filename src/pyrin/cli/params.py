# -*- coding: utf-8 -*-
"""
cli params module.
"""

from pyrin.cli.arguments import ArgumentBase, BooleanArgument


class CLIParamBase(ArgumentBase):
    """
    cli param base class.

    all cli param classes must be subclassed from this.
    """

    def process_inputs(self, **options):
        """
        processes the inputs in given dict.

        :rtype: dict
        """

        return self._process_inputs(**options)

    def _process_inputs(self, **options):
        """
        processes the inputs in given dict.

        subclasses could override this method and modify inputs as needed.
        if the modification is a static one, you could provide default in
        the param initialization, but if the modification is not static,
        for example, a callable must be used to generate value based on
        current situation, you must override this method to modify inputs and
        inject the correct value. subclasses must call `super()._process_inputs(**options)`
        after their work has be done.

        :rtype: dict
        """

        return options


class HelpParam(BooleanArgument, CLIParamBase):
    """
    help param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of HelpParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('help', '--help', default=default)


class VerboseParam(BooleanArgument, CLIParamBase):
    """
    verbose param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of VerboseParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('verbose', '--verbose', default=default)
