# -*- coding: utf-8 -*-
"""
babel handlers params module.
"""

from pyrin.cli.metadata import KeywordArgumentMetadata, BooleanArgumentMetadata
from pyrin.globalization.locale.babel.interface import BabelCLIHandlerBase


class BabelCLIParamMixin(BabelCLIHandlerBase):
    """
    babel cli param mixin class.
    all babel param mixin classes must be subclassed from this.
    """
    pass


class DomainParamMixin(BabelCLIParamMixin):
    """
    domain param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        domain = KeywordArgumentMetadata('domain', '--domain')
        self._add_argument_metadata(domain)
        super()._process_arguments()


class InputFileParamMixin(BabelCLIParamMixin):
    """
    input file param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        input_file = KeywordArgumentMetadata('input_file', '--input-file')
        self._add_argument_metadata(input_file)
        super()._process_arguments()


class OutputDirectoryParamMixin(BabelCLIParamMixin):
    """
    output directory param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        output_dir = KeywordArgumentMetadata('output_dir', '--output-dir')
        self._add_argument_metadata(output_dir)
        super()._process_arguments()


class OmitHeaderParamMixin(BabelCLIParamMixin):
    """
    omit header param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        omit_header = BooleanArgumentMetadata('omit_header', '--omit-header')
        self._add_argument_metadata(omit_header)
        super()._process_arguments()


class LocaleParamMixin(BabelCLIParamMixin):
    """
    locale param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        locale = KeywordArgumentMetadata('locale', '--locale')
        self._add_argument_metadata(locale)
        super()._process_arguments()


class WidthParamMixin(BabelCLIParamMixin):
    """
    width param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        width = KeywordArgumentMetadata('width', '--width')
        self._add_argument_metadata(width)
        super()._process_arguments()


class NoWrapParamMixin(BabelCLIParamMixin):
    """
    no wrap param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        no_wrap = BooleanArgumentMetadata('no_wrap', '--no-wrap')
        self._add_argument_metadata(no_wrap)
        super()._process_arguments()


class IgnoreObsoleteParamMixin(BabelCLIParamMixin):
    """
    ignore obsolete param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        ignore_obsolete = BooleanArgumentMetadata('ignore_obsolete', '--ignore-obsolete')
        self._add_argument_metadata(ignore_obsolete)
        super()._process_arguments()


class NoFuzzyMatchingParamMixin(BabelCLIParamMixin):
    """
    no fuzzy matching param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        no_fuzzy_matching = BooleanArgumentMetadata('no_fuzzy_matching', '--no-fuzzy-matching')
        self._add_argument_metadata(no_fuzzy_matching)
        super()._process_arguments()


class UpdateHeaderCommentParamMixin(BabelCLIParamMixin):
    """
    update header comment param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        update_header_comment = BooleanArgumentMetadata('update_header_comment',
                                                        '--update-header-comment')
        self._add_argument_metadata(update_header_comment)
        super()._process_arguments()


class PreviousParamMixin(BabelCLIParamMixin):
    """
    previous param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        previous = BooleanArgumentMetadata('previous', '--previous')
        self._add_argument_metadata(previous)
        super()._process_arguments()


class CharsetParamMixin(BabelCLIParamMixin):
    """
    charset param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        charset = KeywordArgumentMetadata('charset', '--charset')
        self._add_argument_metadata(charset)
        super()._process_arguments()


class KeywordsParamMixin(BabelCLIParamMixin):
    """
    keywords param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        keywords = KeywordArgumentMetadata('keywords', '--keywords')
        self._add_argument_metadata(keywords)
        super()._process_arguments()


class NoDefaultKeywordsParamMixin(BabelCLIParamMixin):
    """
    no default keywords param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        no_default_keywords = BooleanArgumentMetadata('no_default_keywords',
                                                      '--no-default-keywords')
        self._add_argument_metadata(no_default_keywords)
        super()._process_arguments()


class MappingParamMixin(BabelCLIParamMixin):
    """
    mapping param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        mapping = KeywordArgumentMetadata('mapping', '--mapping')
        self._add_argument_metadata(mapping)
        super()._process_arguments()


class NoLocationParamMixin(BabelCLIParamMixin):
    """
    no location param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        no_location = BooleanArgumentMetadata('no_location', '--no-location')
        self._add_argument_metadata(no_location)
        super()._process_arguments()


class AddLocationParamMixin(BabelCLIParamMixin):
    """
    add location param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        add_location = KeywordArgumentMetadata('add_location', '--add-location')
        self._add_argument_metadata(add_location)
        super()._process_arguments()


class SortOutputParamMixin(BabelCLIParamMixin):
    """
    sort output param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        sort_output = BooleanArgumentMetadata('sort_output', '--sort-output')
        self._add_argument_metadata(sort_output)
        super()._process_arguments()


class SortByFileParamMixin(BabelCLIParamMixin):
    """
    sort by file param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        sort_by_file = BooleanArgumentMetadata('sort_by_file', '--sort-by-file')
        self._add_argument_metadata(sort_by_file)
        super()._process_arguments()


class MSGIDBugsAddressParamMixin(BabelCLIParamMixin):
    """
    msgid bugs address param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        msgid_bugs_address = KeywordArgumentMetadata('msgid_bugs_address',
                                                     '--msgid-bugs-address')
        self._add_argument_metadata(msgid_bugs_address)
        super()._process_arguments()


class CopyrightHolderParamMixin(BabelCLIParamMixin):
    """
    copyright holder param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        copyright_holder = KeywordArgumentMetadata('copyright_holder',
                                                   '--copyright-holder')
        self._add_argument_metadata(copyright_holder)
        super()._process_arguments()


class ProjectParamMixin(BabelCLIParamMixin):
    """
    project param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        project = KeywordArgumentMetadata('project', '--project')
        self._add_argument_metadata(project)
        super()._process_arguments()


class VersionParamMixin(BabelCLIParamMixin):
    """
    version param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        version = KeywordArgumentMetadata('version', '--version')
        self._add_argument_metadata(version)
        super()._process_arguments()


class AddCommentsParamMixin(BabelCLIParamMixin):
    """
    add comments param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        add_comments = KeywordArgumentMetadata('add_comments', '--add-comments')
        self._add_argument_metadata(add_comments)
        super()._process_arguments()


class StripCommentsParamMixin(BabelCLIParamMixin):
    """
    strip comments param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        strip_comments = BooleanArgumentMetadata('strip_comments', '--strip-comments')
        self._add_argument_metadata(strip_comments)
        super()._process_arguments()


class InputDirsParamMixin(BabelCLIParamMixin):
    """
    input dirs param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        input_dirs = KeywordArgumentMetadata('input_dirs', '--input-dirs')
        self._add_argument_metadata(input_dirs)
        super()._process_arguments()


class DirectoryParamMixin(BabelCLIParamMixin):
    """
    directory param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        directory = KeywordArgumentMetadata('directory', '--directory')
        self._add_argument_metadata(directory)
        super()._process_arguments()


class UseFuzzyParamMixin(BabelCLIParamMixin):
    """
    use fuzzy param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        use_fuzzy = BooleanArgumentMetadata('use_fuzzy', '--use-fuzzy')
        self._add_argument_metadata(use_fuzzy)
        super()._process_arguments()


class StatisticsParamMixin(BabelCLIParamMixin):
    """
    statistics param mixin class.
    """

    def _process_arguments(self):
        """
        processes the options that are related to this handler.
        """

        statistics = BooleanArgumentMetadata('statistics', '--statistics')
        self._add_argument_metadata(statistics)
        super()._process_arguments()
