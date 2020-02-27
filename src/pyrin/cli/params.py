# -*- coding: utf-8 -*-
"""
cli params module.
"""

from pyrin.cli.base import CLIHandlerOptionsMetadata, CLIHandlerBase


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

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        help_option = CLIHandlerOptionsMetadata('help', None, {True: '--help', False: None})
        self._add_options_metadata(help_option)
        super()._process_options()


class VerboseParamMixin(CLIParamMixin):
    """
    verbose param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        verbose = CLIHandlerOptionsMetadata('verbose', None, {True: '--verbose', False: None})
        self._add_options_metadata(verbose)
        super()._process_options()
