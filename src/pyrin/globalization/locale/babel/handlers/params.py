# -*- coding: utf-8 -*-
"""
babel handlers params module.
"""

import os

import pyrin.configuration.services as config_services
import pyrin.application.services as application_services
import pyrin.globalization.locale.babel.services as babel_services

from pyrin.globalization.locale.babel.interface import BabelCLIParamBase
from pyrin.cli.arguments import KeywordArgument, BooleanArgument, \
    PositionalArgument, CompositeKeywordArgument


class DomainParam(KeywordArgument, BabelCLIParamBase):
    """
    domain param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of DomainParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `domain` value form babel
                               config store if not provided.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'domain')

        super().__init__('domain', '--domain', default=default)


class CompileDomainsParam(CompositeKeywordArgument, BabelCLIParamBase):
    """
    compile domains param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of CompileDomainsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `compile_domains` value form
                               babel config store if not provided.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'compile_domains')

        super().__init__('domain', '--domain', default=default)


class InputTemplateFileParam(KeywordArgument, BabelCLIParamBase):
    """
    input template file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of InputTemplateFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `locale_path/template_file`
                               where `template_file` comes from
                               babel config store.
        """

        if default is None:
            default = os.path.join(application_services.get_locale_path(),
                                   config_services.get('babel', 'arguments', 'template_file'))

        super().__init__('input_file', '--input-file', default=default)


class OutputDirectoryParam(KeywordArgument, BabelCLIParamBase):
    """
    output directory param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of OutputDirectoryParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `locale_path` of application.
        """

        if default is None:
            default = application_services.get_locale_path()

        super().__init__('output_dir', '--output-dir', default=default)


class OutputTemplateFileParam(KeywordArgument, BabelCLIParamBase):
    """
    output template file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of OutputTemplateFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `locale_path/template_file`
                               where `template_file` comes from
                               babel config store.
        """

        if default is None:
            default = os.path.join(application_services.get_locale_path(),
                                   config_services.get('babel', 'arguments', 'template_file'))

        super().__init__('output_file', '--output-file', default=default)


class OutputFileParam(KeywordArgument, BabelCLIParamBase):
    """
    output file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of OutputFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to None.
        """

        super().__init__('output_file', '--output-file', default=default)


class OmitHeaderParam(BooleanArgument, BabelCLIParamBase):
    """
    omit header param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of OmitHeaderParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `omit_header`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'omit_header')

        super().__init__('omit_header', '--omit-header', default=default)


class LocaleParam(KeywordArgument, BabelCLIParamBase):
    """
    locale param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of LocaleParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to None.
        """

        super().__init__('locale', '--locale', default=default)


class WidthParam(KeywordArgument, BabelCLIParamBase):
    """
    width param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of WidthParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `width`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'width')

        super().__init__('width', '--width', default=default)


class NoWrapParam(BooleanArgument, BabelCLIParamBase):
    """
    no wrap param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of NoWrapParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `no_wrap`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'no_wrap')

        super().__init__('no_wrap', '--no-wrap', default=default)


class IgnoreObsoleteParam(BooleanArgument, BabelCLIParamBase):
    """
    ignore obsolete param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of IgnoreObsoleteParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `ignore_obsolete`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'ignore_obsolete')

        super().__init__('ignore_obsolete', '--ignore-obsolete', default=default)


class NoFuzzyMatchingParam(BooleanArgument, BabelCLIParamBase):
    """
    no fuzzy matching param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of NoFuzzyMatchingParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `no_fuzzy_matching`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'no_fuzzy_matching')

        super().__init__('no_fuzzy_matching', '--no-fuzzy-matching', default=default)


class UpdateHeaderCommentParam(BooleanArgument, BabelCLIParamBase):
    """
    update header comment param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of UpdateHeaderCommentParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `update_header_comment`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'update_header_comment')

        super().__init__('update_header_comment', '--update-header-comment', default=default)


class PreviousParam(BooleanArgument, BabelCLIParamBase):
    """
    previous param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of PreviousParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `previous`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'previous')

        super().__init__('previous', '--previous', default=default)


class CharsetParam(KeywordArgument, BabelCLIParamBase):
    """
    charset param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of CharsetParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `charset`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'charset')

        super().__init__('charset', '--charset', default=default)


class KeywordsParam(CompositeKeywordArgument, BabelCLIParamBase):
    """
    keywords param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of KeywordsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `keywords`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'keywords')

        super().__init__('keywords', '--keywords', default=default)


class NoDefaultKeywordsParam(BooleanArgument, BabelCLIParamBase):
    """
    no default keywords param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of NoDefaultKeywordsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `no_default_keywords`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'no_default_keywords')

        super().__init__('no_default_keywords', '--no-default-keywords', default=default)


class MappingParam(KeywordArgument, BabelCLIParamBase):
    """
    mapping param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of MappingParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               path to `babel.mappings.ini`.
        """

        if default is None:
            package = babel_services.get_package_class()
            default = config_services.get_file_path(package.EXTRA_CONFIG_STORE_NAMES[0])

        super().__init__('mapping', '--mapping', default=default)


class NoLocationParam(BooleanArgument, BabelCLIParamBase):
    """
    no location param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of NoLocationParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `no_location`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'no_location')

        super().__init__('no_location', '--no-location', default=default)


class AddLocationParam(KeywordArgument, BabelCLIParamBase):
    """
    add location param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of AddLocationParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `add_location`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'add_location')

        super().__init__('add_location', '--add-location', default=default)


class SortOutputParam(BooleanArgument, BabelCLIParamBase):
    """
    sort output param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of SortOutputParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `sort_output`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'sort_output')

        super().__init__('sort_output', '--sort-output', default=default)


class SortByFileParam(BooleanArgument, BabelCLIParamBase):
    """
    sort by file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of SortByFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `sort_by_file`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'sort_by_file')

        super().__init__('sort_by_file', '--sort-by-file', default=default)


class MSGIDBugsAddressParam(KeywordArgument, BabelCLIParamBase):
    """
    msgid bugs address param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of MSGIDBugsAddressParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `msgid_bugs_address`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'msgid_bugs_address')

        super().__init__('msgid_bugs_address', '--msgid-bugs-address', default=default)


class CopyrightHolderParam(KeywordArgument, BabelCLIParamBase):
    """
    copyright holder param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of CopyrightHolderParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `copyright_holder`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'copyright_holder')

        super().__init__('copyright_holder', '--copyright-holder', default=default)


class ProjectParam(KeywordArgument, BabelCLIParamBase):
    """
    project param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ProjectParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `project`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'project')

        super().__init__('project', '--project', default=default)


class VersionParam(KeywordArgument, BabelCLIParamBase):
    """
    version param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of VersionParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `version`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'version')

        super().__init__('version', '--version', default=default)


class AddCommentsParam(CompositeKeywordArgument, BabelCLIParamBase):
    """
    add comments param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of AddCommentsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `add_comments`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'add_comments')

        super().__init__('add_comments', '--add-comments', default=default)


class StripCommentsParam(BooleanArgument, BabelCLIParamBase):
    """
    strip comments param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of StripCommentsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `strip_comments`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'strip_comments')

        super().__init__('strip_comments', '--strip-comments', default=default)


class InputPathsParam(PositionalArgument, BabelCLIParamBase):
    """
    input paths param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of InputPathsParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to both application and pyrin
                               main package paths if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        if default is None:
            default = self._get_paths(include_application=True, include_pyrin=True)

        super().__init__('input_paths', index, default=default, **options)

    def _process_inputs(self, **options):
        """
        processes the inputs given to this handler and returns them.

        :rtype: dict
        """

        include_application = options.get('include_app', False)
        include_pyrin = options.get('include_pyrin', False)
        paths = self._get_paths(include_application, include_pyrin)

        if len(paths) <= 0:
            paths = None

        options.update(input_paths=paths)
        return super()._process_inputs(**options)

    def _get_paths(self, include_application=True, include_pyrin=True):
        """
        gets application and pyrin main package paths based on given inputs.

        :param bool include_application: include application main package path.
                                         defaults to True if not provided.

        :param bool include_pyrin: include pyrin main package path.
                                   defaults to True if not provided.

        :rtype: list[str]
        """

        paths = []
        if include_application is True:
            paths.append(application_services.get_application_main_package_path())

        if include_pyrin is True:
            paths.append(application_services.get_pyrin_main_package_path())

        return paths


class DirectoryParam(KeywordArgument, BabelCLIParamBase):
    """
    directory param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of DirectoryParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to
                               `locale_path` of application.
        """

        if default is None:
            default = application_services.get_locale_path()

        super().__init__('directory', '--directory', default=default)


class UseFuzzyParam(BooleanArgument, BabelCLIParamBase):
    """
    use fuzzy param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of UseFuzzyParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to `use_fuzzy`
                               value from babel config store.
        """

        if default is None:
            default = config_services.get('babel', 'arguments', 'use_fuzzy')

        super().__init__('use_fuzzy', '--use-fuzzy', default=default)


class StatisticsParam(BooleanArgument, BabelCLIParamBase):
    """
    statistics param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of StatisticsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               if not provided, defaults to None.
        """

        super().__init__('statistics', '--statistics', default=default)
