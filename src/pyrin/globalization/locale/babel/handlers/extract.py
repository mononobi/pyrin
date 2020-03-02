# -*- coding: utf-8 -*-
"""
babel handlers extract module.
"""

from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import OmitHeaderParamMixin, \
    WidthParamMixin, NoWrapParamMixin, CharsetParamMixin, KeywordsParamMixin, \
    NoDefaultKeywordsParamMixin, MappingParamMixin, NoLocationParamMixin, \
    AddLocationParamMixin, SortOutputParamMixin, SortByFileParamMixin, \
    MSGIDBugsAddressParamMixin, CopyrightHolderParamMixin, ProjectParamMixin, \
    VersionParamMixin, AddCommentsParamMixin, StripCommentsParamMixin, InputDirsParamMixin


@babel_cli_handler()
class ExtractCLIHandler(OmitHeaderParamMixin, WidthParamMixin,
                        NoWrapParamMixin, CharsetParamMixin,
                        KeywordsParamMixin, NoDefaultKeywordsParamMixin,
                        MappingParamMixin, NoLocationParamMixin,
                        AddLocationParamMixin, SortOutputParamMixin,
                        SortByFileParamMixin, MSGIDBugsAddressParamMixin,
                        CopyrightHolderParamMixin, ProjectParamMixin,
                        VersionParamMixin, AddCommentsParamMixin,
                        StripCommentsParamMixin, InputDirsParamMixin):
    """
    extract cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ExtractCLIHandler.
        """

        super().__init__('extract')
