# -*- coding: utf-8 -*-
"""
babel interface module.
"""

from pyrin.cli.base import CLIHandlerBase
from pyrin.cli.params import CLIParamBase


class BabelCLIParamBase(CLIParamBase):
    """
    babel cli param base class.

    all babel cli param classes must be subclassed from this.
    """
    pass


class BabelCLIHandlerBase(CLIHandlerBase):
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
