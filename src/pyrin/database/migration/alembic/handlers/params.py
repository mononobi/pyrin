# -*- coding: utf-8 -*-
"""
alembic handlers params module.
"""

import pyrin.globalization.datetime.services as datetime_services
import pyrin.configuration.services as config_services

from pyrin.cli.arguments import BooleanArgument, KeywordArgument, PositionalArgument
from pyrin.database.migration.alembic.interface import AlembicCLIParamBase


class SQLParam(BooleanArgument, AlembicCLIParamBase):
    """
    sql param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of SQLParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('sql', '--sql', default=default)


class TagParam(KeywordArgument, AlembicCLIParamBase):
    """
    tag param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of TagParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('tag', '--tag', default=default)


class RevisionParam(PositionalArgument, AlembicCLIParamBase):
    """
    revision param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of RevisionParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('revision', index, default=default, **options)


class ResolveDependenciesParam(BooleanArgument, AlembicCLIParamBase):
    """
    resolve dependencies param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ResolveDependenciesParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('resolve_dependencies', '--resolve-dependencies', default=default)


class IndicateCurrentParam(BooleanArgument, AlembicCLIParamBase):
    """
    indicate current param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of IndicateCurrentParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('indicate_current', '--indicate-current', default=default)


class RevisionRangeParam(KeywordArgument, AlembicCLIParamBase):
    """
    revision range param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of RevisionRangeParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('revision_range', '--rev-range', default=default)


class MessageParam(KeywordArgument, AlembicCLIParamBase):
    """
    message param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of MessageParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('message', '--message', default=default)

    def _process_inputs(self, **options):
        """
        processes the inputs in given dict.

        :rtype: dict
        """

        if options.get('message', None) is None:
            timezone = config_services.get('alembic', 'alembic', 'timezone')
            message = datetime_services.get_current_timestamp(date_sep=None,
                                                              main_sep=None,
                                                              time_sep=None,
                                                              timezone=timezone)
            options.update(message=message)

        return super()._process_inputs(**options)


class BranchLabelParam(KeywordArgument, AlembicCLIParamBase):
    """
    branch label param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of BranchLabelParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('branch_label', '--branch-label', default=default)


class RevisionIDParam(KeywordArgument, AlembicCLIParamBase):
    """
    revision id param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of RevisionIDParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('revision_id', '--rev-id', default=default)


class RevisionsParam(PositionalArgument, AlembicCLIParamBase):
    """
    revisions param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of RevisionsParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('revisions', index, default=default, **options)


class AutoGenerateParam(BooleanArgument, AlembicCLIParamBase):
    """
    autogenerate param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of AutoGenerateParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('autogenerate', '--autogenerate', default=default)


class HeadParam(KeywordArgument, AlembicCLIParamBase):
    """
    head param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of HeadParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('head', '--head', default=default)


class SpliceParam(BooleanArgument, AlembicCLIParamBase):
    """
    splice param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of SpliceParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('splice', '--splice', default=default)


class VersionPathParam(KeywordArgument, AlembicCLIParamBase):
    """
    version path param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of VersionPathParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('version_path', '--version-path', default=default)


class DependsOnParam(KeywordArgument, AlembicCLIParamBase):
    """
    depends on param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of DependsOnParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('depends_on', '--depends-on', default=default)


class PurgeParam(BooleanArgument, AlembicCLIParamBase):
    """
    purge param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of PurgeParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.
        """

        super().__init__('purge', '--purge', default=default)
