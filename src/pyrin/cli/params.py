# -*- coding: utf-8 -*-
"""
cli params module.
"""

from pyrin.cli.base import CLIHandlerBase
from pyrin.cli.metadata import BooleanArgumentMetadata


class CLIParamMixin(CLIHandlerBase):
    """
    cli param mixin class.
    all param mixin classes must be subclassed from this.
    """
    pass


class HelpParamMixin(CLIParamMixin):
    """
    help param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        help_option = BooleanArgumentMetadata('help', '--help')
        self._add_argument_metadata(help_option)
        super()._process_arguments()


class VerboseParamMixin(CLIParamMixin):
    """
    verbose param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        verbose = BooleanArgumentMetadata('verbose', '--verbose')
        self._add_argument_metadata(verbose)
        super()._process_arguments()
