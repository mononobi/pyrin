# -*- coding: utf-8 -*-
"""
babel handlers compile module.
"""

from pyrin.globalization.locale.babel.enumerations import BabelCLIHandlersEnum
from pyrin.globalization.locale.babel.interface import BabelCLIHandlerBase
from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import LocaleParam, \
    UseFuzzyParam, StatisticsParam, DirectoryParam, CompileDomainsParam, OutputFileParam


@babel_cli_handler()
class CompileCLIHandler(BabelCLIHandlerBase):
    """
    compile cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of CompileCLIHandler.
        """

        super().__init__(BabelCLIHandlersEnum.COMPILE)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([LocaleParam(), CompileDomainsParam(),
                       UseFuzzyParam(), StatisticsParam(),
                       DirectoryParam(), OutputFileParam()])

        return super()._inject_params(params)
