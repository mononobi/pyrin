# -*- coding: utf-8 -*-
"""
babel handlers update module.
"""

from pyrin.globalization.locale.babel.enumerations import BabelCLIHandlersEnum
from pyrin.globalization.locale.babel.interface import BabelCLIHandlerBase
from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import DomainParam, \
    InputTemplateFileParam, OutputDirectoryParam, OmitHeaderParam, LocaleParam, \
    WidthParam, NoWrapParam, IgnoreObsoleteParam, NoFuzzyMatchingParam, \
    UpdateHeaderCommentParam, PreviousParam, OutputFileParam


@babel_cli_handler()
class UpdateCLIHandler(BabelCLIHandlerBase):
    """
    update cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of UpdateCLIHandler.
        """

        super().__init__(BabelCLIHandlersEnum.UPDATE)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([DomainParam(), InputTemplateFileParam(),
                       OmitHeaderParam(), LocaleParam(),
                       WidthParam(), OutputDirectoryParam(),
                       NoWrapParam(), NoFuzzyMatchingParam(),
                       IgnoreObsoleteParam(), PreviousParam(),
                       UpdateHeaderCommentParam(), OutputFileParam()])

        return super()._inject_params(params)
