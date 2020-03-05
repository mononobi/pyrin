# -*- coding: utf-8 -*-
"""
babel handlers compile module.
"""

from pyrin.globalization.locale.babel.interface import BabelCLIHandlerBase
from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import InputTemplateFileParam, \
    LocaleParam, UseFuzzyParam, StatisticsParam, DirectoryParam, CompileDomainsParam


@babel_cli_handler()
class CompileCLIHandler(BabelCLIHandlerBase):
    """
    compile cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of CompileCLIHandler.
        """

        super().__init__('compile')

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([InputTemplateFileParam(), LocaleParam(),
                       UseFuzzyParam(), StatisticsParam(),
                       DirectoryParam(), CompileDomainsParam()])

        return super()._inject_params(params)
