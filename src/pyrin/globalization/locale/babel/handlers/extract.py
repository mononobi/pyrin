# -*- coding: utf-8 -*-
"""
babel handlers extract module.
"""

from pyrin.globalization.locale.babel.enumerations import BabelCLIHandlersEnum
from pyrin.globalization.locale.babel.interface import BabelCLIHandlerBase
from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import OmitHeaderParam, \
    WidthParam, NoWrapParam, CharsetParam, KeywordsParam, NoDefaultKeywordsParam, \
    MappingParam, NoLocationParam, AddLocationParam, SortOutputParam, SortByFileParam, \
    MSGIDBugsAddressParam, CopyrightHolderParam, ProjectParam, VersionParam, \
    AddCommentsParam, StripCommentsParam, InputPathsParam, OutputTemplateFileParam


@babel_cli_handler()
class ExtractCLIHandler(BabelCLIHandlerBase):
    """
    extract cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ExtractCLIHandler.
        """

        super().__init__(BabelCLIHandlersEnum.EXTRACT)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([OmitHeaderParam(), WidthParam(), NoWrapParam(),
                       CharsetParam(), KeywordsParam(), NoDefaultKeywordsParam(),
                       MappingParam(), NoLocationParam(), AddLocationParam(),
                       SortOutputParam(), SortByFileParam(), MSGIDBugsAddressParam(),
                       CopyrightHolderParam(), ProjectParam(), VersionParam(),
                       AddCommentsParam(), StripCommentsParam(), InputPathsParam(),
                       OutputTemplateFileParam()])

        return super()._inject_params(params)
