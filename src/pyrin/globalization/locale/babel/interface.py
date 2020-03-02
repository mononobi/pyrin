# -*- coding: utf-8 -*-
"""
babel interface module.
"""

from pyrin.cli.metadata import KeywordArgumentMetadata
from pyrin.cli.params import HelpParamMixin


class BabelCLIHandlerBase(HelpParamMixin):
    """
    babel cli handler base class.
    all babel cli handlers must be subclassed from this.
    """

    def __init__(self, name):
        """
        initializes an instance of BabelCLIHandlerBase.

        :param str name: the handler name that should be registered
                         with. this name must be the exact name that
                         this handler must emmit to cli.
        """

        super().__init__(name)

    def _get_common_cli_options(self):
        """
        gets the list of common cli options.

        :rtype: list
        """

        return ['pybabel']

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        output_file = KeywordArgumentMetadata('output_file', '--output-file')
        self._add_argument_metadata(output_file)
        super()._process_arguments()
