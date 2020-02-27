# -*- coding: utf-8 -*-
"""
database migration alembic handlers params module.
"""

from pyrin.cli.base import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


class AlembicCLIParamMixin(AlembicCLIHandlerBase):
    """
    alembic cli param mixin class.
    all alembic param mixin classes must be subclassed from this.
    """
    pass


class SQLParamMixin(AlembicCLIParamMixin):
    """
    sql param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        sql = CLIHandlerOptionsMetadata('sql', None, {True: '--sql', False: None})
        self._add_options_metadata(sql)
        super()._process_options()


class TagParamMixin(AlembicCLIParamMixin):
    """
    tag param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        tag = CLIHandlerOptionsMetadata('tag', '--tag')
        self._add_options_metadata(tag)
        super()._process_options()


class RevisionParamMixin(AlembicCLIParamMixin):
    """
    revision param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        revision = CLIHandlerOptionsMetadata('revision', None)
        self._add_options_metadata(revision)
        super()._process_options()


class ResolveDependenciesParamMixin(AlembicCLIParamMixin):
    """
    resolve dependencies param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        resolve_dependencies = CLIHandlerOptionsMetadata('resolve_dependencies', None,
                                                         {True: '--resolve-dependencies',
                                                          False: None})
        self._add_options_metadata(resolve_dependencies)
        super()._process_options()


class IndicateCurrentParamMixin(AlembicCLIParamMixin):
    """
    indicate current param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        indicate_current = CLIHandlerOptionsMetadata('indicate_current', None,
                                                     {True: '--indicate-current',
                                                      False: None})
        self._add_options_metadata(indicate_current)
        super()._process_options()


class RevisionRangeParamMixin(AlembicCLIParamMixin):
    """
    revision range param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        revision_range = CLIHandlerOptionsMetadata('revision_range', '--rev-range')
        self._add_options_metadata(revision_range)
        super()._process_options()


class MessageParamMixin(AlembicCLIParamMixin):
    """
    message param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        message = CLIHandlerOptionsMetadata('message', '--message')
        self._add_options_metadata(message)
        super()._process_options()


class BranchLabelParamMixin(AlembicCLIParamMixin):
    """
    branch label param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        branch_label = CLIHandlerOptionsMetadata('branch_label', '--branch-label')
        self._add_options_metadata(branch_label)
        super()._process_options()


class RevisionIDParamMixin(AlembicCLIParamMixin):
    """
    revision id param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        revision_id = CLIHandlerOptionsMetadata('revision_id', '--rev-id')
        self._add_options_metadata(revision_id)
        super()._process_options()


class RevisionsParamMixin(AlembicCLIParamMixin):
    """
    revisions param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        revisions = CLIHandlerOptionsMetadata('revisions', None)
        self._add_options_metadata(revisions)
        super()._process_options()


class AutoGenerateParamMixin(AlembicCLIParamMixin):
    """
    autogenerate param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        autogenerate = CLIHandlerOptionsMetadata('autogenerate', None,
                                                 {True: '--autogenerate', False: None})
        self._add_options_metadata(autogenerate)
        super()._process_options()


class HeadParamMixin(AlembicCLIParamMixin):
    """
    head param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        head = CLIHandlerOptionsMetadata('head', '--head')
        self._add_options_metadata(head)
        super()._process_options()


class SpliceParamMixin(AlembicCLIParamMixin):
    """
    splice param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        splice = CLIHandlerOptionsMetadata('splice', None, {True: '--splice', False: None})
        self._add_options_metadata(splice)
        super()._process_options()


class VersionPathParamMixin(AlembicCLIParamMixin):
    """
    version path param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        version_path = CLIHandlerOptionsMetadata('version_path', '--version-path')
        self._add_options_metadata(version_path)
        super()._process_options()


class DependsOnParamMixin(AlembicCLIParamMixin):
    """
    depends on param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        depends_on = CLIHandlerOptionsMetadata('depends_on', '--depends-on')
        self._add_options_metadata(depends_on)
        super()._process_options()


class PurgeParamMixin(AlembicCLIParamMixin):
    """
    purge param mixin class.
    """

    def _process_options(self):
        """
        processes the options that are related to this handler.
        """

        purge = CLIHandlerOptionsMetadata('purge', None, {True: '--purge', False: None})
        self._add_options_metadata(purge)
        super()._process_options()
