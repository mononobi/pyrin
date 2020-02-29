# -*- coding: utf-8 -*-
"""
database migration alembic handlers params module.
"""

from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase
from pyrin.cli.metadata import BooleanArgumentMetadata, KeywordArgumentMetadata, \
    PositionalArgumentMetadata


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

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        sql = BooleanArgumentMetadata('sql', '--sql')
        self._add_argument_metadata(sql)
        super()._process_arguments()


class TagParamMixin(AlembicCLIParamMixin):
    """
    tag param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        tag = KeywordArgumentMetadata('tag', '--tag')
        self._add_argument_metadata(tag)
        super()._process_arguments()


class RevisionParamMixin(AlembicCLIParamMixin):
    """
    revision param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        revision = PositionalArgumentMetadata('revision', 0)
        self._add_argument_metadata(revision)
        super()._process_arguments()


class ResolveDependenciesParamMixin(AlembicCLIParamMixin):
    """
    resolve dependencies param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        resolve_dependencies = BooleanArgumentMetadata('resolve_dependencies',
                                                       '--resolve-dependencies')
        self._add_argument_metadata(resolve_dependencies)
        super()._process_arguments()


class IndicateCurrentParamMixin(AlembicCLIParamMixin):
    """
    indicate current param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        indicate_current = BooleanArgumentMetadata('indicate_current', '--indicate-current')
        self._add_argument_metadata(indicate_current)
        super()._process_arguments()


class RevisionRangeParamMixin(AlembicCLIParamMixin):
    """
    revision range param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        revision_range = KeywordArgumentMetadata('revision_range', '--rev-range')
        self._add_argument_metadata(revision_range)
        super()._process_arguments()


class MessageParamMixin(AlembicCLIParamMixin):
    """
    message param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        message = KeywordArgumentMetadata('message', '--message')
        self._add_argument_metadata(message)
        super()._process_arguments()


class BranchLabelParamMixin(AlembicCLIParamMixin):
    """
    branch label param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        branch_label = KeywordArgumentMetadata('branch_label', '--branch-label')
        self._add_argument_metadata(branch_label)
        super()._process_arguments()


class RevisionIDParamMixin(AlembicCLIParamMixin):
    """
    revision id param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        revision_id = KeywordArgumentMetadata('revision_id', '--rev-id')
        self._add_argument_metadata(revision_id)
        super()._process_arguments()


class RevisionsParamMixin(AlembicCLIParamMixin):
    """
    revisions param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        revisions = PositionalArgumentMetadata('revisions', 0)
        self._add_argument_metadata(revisions)
        super()._process_arguments()


class AutoGenerateParamMixin(AlembicCLIParamMixin):
    """
    autogenerate param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        autogenerate = BooleanArgumentMetadata('autogenerate', '--autogenerate')
        self._add_argument_metadata(autogenerate)
        super()._process_arguments()


class HeadParamMixin(AlembicCLIParamMixin):
    """
    head param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        head = KeywordArgumentMetadata('head', '--head')
        self._add_argument_metadata(head)
        super()._process_arguments()


class SpliceParamMixin(AlembicCLIParamMixin):
    """
    splice param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        splice = BooleanArgumentMetadata('splice', '--splice')
        self._add_argument_metadata(splice)
        super()._process_arguments()


class VersionPathParamMixin(AlembicCLIParamMixin):
    """
    version path param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        version_path = KeywordArgumentMetadata('version_path', '--version-path')
        self._add_argument_metadata(version_path)
        super()._process_arguments()


class DependsOnParamMixin(AlembicCLIParamMixin):
    """
    depends on param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        depends_on = KeywordArgumentMetadata('depends_on', '--depends-on')
        self._add_argument_metadata(depends_on)
        super()._process_arguments()


class PurgeParamMixin(AlembicCLIParamMixin):
    """
    purge param mixin class.
    """

    def _process_arguments(self):
        """
        processes the arguments that are related to this handler.
        """

        purge = BooleanArgumentMetadata('purge', '--purge')
        self._add_argument_metadata(purge)
        super()._process_arguments()
