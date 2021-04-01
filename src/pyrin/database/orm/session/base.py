# -*- coding: utf-8 -*-
"""
orm session base module.
"""

from sqlalchemy.orm import Session
from sqlalchemy.util import EMPTY_DICT
from sqlalchemy.sql.elements import TextClause

import pyrin.database.services as database_services
import pyrin.database.orm.sql.extractor.services as extractor_services

from pyrin.core.globals import _
from pyrin.core.structs import CoreObject
from pyrin.database.exceptions import InvalidDatabaseBindError
from pyrin.database.orm.session.exceptions import TransientSQLExpressionRequiredError


class CoreSession(Session, CoreObject):
    """
    core session class.

    all application sessions must be an instance this.
    """

    # these keywords are forbidden when 'execute' method is called
    # with 'transient=True' and a raw sql is given.
    NON_TRANSIENT_KEYWORDS = ('commit', 'flush', 'rollback', 'alter ', 'create ', 'drop ')

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreSession.

        all positional and keyword arguments will be passed to underlying `Session`
        class. for details on inputs, see `Session` docstrings.

        :param object args: all positional arguments.

        :keyword object kwargs: all keyword arguments.

        :keyword bool atomic: specifies that this session is an atomic session.
                              defaults to False if not provided.
        """

        self._atomic = kwargs.pop('atomic', False)

        super().__init__(*args, **kwargs)

        # we have to manually call '__init__' on CoreObject because 'Session'
        # does not call 'super().__init__()' in its '__init__' method.
        CoreObject.__init__(self)

    def __str__(self):
        """
        gets the string representation of current session.

        :rtype: str
        """

        return '{fullname}: atomic={atomic}'.format(fullname=self.get_fully_qualified_name(),
                                                    atomic=self.atomic)

    def execute(self, statement, params=None,
                execution_options=EMPTY_DICT, bind_arguments=None,
                _parent_execute_state=None, _add_event=None, **kw):
        """
        executes a sql expression construct or string statement.

        it will be executed within the current transaction.
        the current transaction will be resolved using the given
        entity class or object or bind name.

        this method is a wrapper for `sqlalchemy.orm.session.execute()` method
        which wraps it to bind to correct engine on different situations.
        for full documentation see the `sqlalchemy.orm.session.execute()` docs.

        :param Executable | str statement: an executable statement `Executable`
                                           expression such as `expression.select`
                                           or string sql statement to be executed.

        :param dict | list[dict] params: optional dictionary, or list of
                                         dictionaries, containing bound
                                         parameter values. if a single dictionary,
                                         single-row execution occurs. if a list of
                                         dictionaries, an `executemany' will be invoked.
                                         the keys in each dictionary must correspond
                                         to parameter names present in the statement.

        :param dict execution_options: optional dictionary of execution options,
                                       which will be associated with the statement execution.
                                       this dictionary can provide a subset of the options that
                                       are accepted by `_future.Connection.execution_options`
                                       method, and may also provide additional options understood
                                       only in an ORM context.

        :param dict bind_arguments: dictionary of additional arguments to determine
                                    the bind. may include `mapper`, `bind` or other custom
                                    arguments. contents of this dictionary are passed to the
                                    `.Session.get_bind` method.

        :param _parent_execute_state: for internal usage.
        :param _add_event: for internal usage.

        :keyword str bind_name: database bind name from `database.binds.ini`
                                file on which given statement must be executed.
                                this keyword argument has precedence over `mapper`
                                and `statement` when locating a bind.

        :keyword bool transient: specifies that raw sql expressions must not affect
                                 the database. if set to True and a raw sql is
                                 given, it could not contain `NON_TRANSIENT_KEYWORDS`.
                                 defaults to False if not provided.

        :raises InvalidDatabaseBindError: invalid database bind error.
        :raises TransientSQLExpressionRequiredError: transient sql expression required error.

        :returns: results of the statement execution.
        :rtype: ResultProxy
        """

        bind = None
        if bind_arguments is not None:
            bind = bind_arguments.get('bind')

        bind_name = kw.pop('bind_name', None)
        if bind is None and bind_name is not None:
            bind = database_services.get_bounded_engines().get(bind_name, None)
            if bind is None:
                raise InvalidDatabaseBindError('Database bind name [{bind_name}] '
                                               'is not available in database.binds '
                                               'config store.'
                                               .format(bind_name=bind_name))

            if bind_arguments is None:
                bind_arguments = dict()

            bind_arguments.update(bind=bind)

        transient = kw.pop('transient', False)
        if transient is True and isinstance(statement, (str, TextClause)):
            raw_sql = None
            if isinstance(statement, TextClause):
                raw_sql = statement.text.lower()
            else:
                raw_sql = statement.lower()

            for item in self.NON_TRANSIENT_KEYWORDS:
                if item in raw_sql:
                    raise TransientSQLExpressionRequiredError(_('Transient sql expressions '
                                                                'should not contain [{keyword}] '
                                                                'keyword.')
                                                              .format(keyword=item.strip()))

        return super().execute(statement, params, execution_options,
                               bind_arguments, _parent_execute_state,
                               _add_event, **kw)

    def get_bind(self, mapper=None, clause=None, bind=None,
                 _sa_skip_events=None, _sa_skip_for_implicit_returning=False):
        """
        returns a `bind` to which this `CoreSession` is bounded.

        this method extends the `get_bind() method of `Session` by
        trying to find bounded engine to tables of a raw string query.

        the `bind` is usually an instance of `Engine`,
        except in the case where the `CoreSession` has been
        explicitly bound directly to a `Connection`.

        for a multiply-bound or unbound `CoreSession`, the
        `mapper` or `clause` arguments are used to determine the
        appropriate bind to return.

        note that the 'mapper' argument is usually present
        when `CoreSession.get_bind` is called via an orm
        operation such as a `Session.query`, each
        individual INSERT/UPDATE/DELETE operation within a
        `Session.flush`, call, etc.

        The order of resolution is:

        1. if mapper given and session.binds is present,
           locate a bind based first on the mapper in use, then
           on the mapped class in use, then on any base classes that are
           present in the `__mro__` of the mapped class, from more specific
           superclasses to more general.
        2. if clause given and session.binds is present,
           locate a bind based on `Table` objects
           found in the given clause present in session.binds.
        3. if session.bind is present, return that.
        4. if clause given, attempt to return a bind
           linked to the `MetaData` ultimately
           associated with the clause.
        5. if mapper given, attempt to return a bind
           linked to the `MetaData` ultimately
           associated with the `Table` or other
           selectable to which the mapper is mapped.
        6. no bind can be found, `sqlalchemy.exc.UnboundExecutionError`
           is raised.

        :param BaseEntity mapper: a BaseEntity instance or class. the bind can be derived from
                                  a `Mapper` first by consulting the `binds` map associated
                                  with this `Session`, and secondly by consulting the
                                  `Metadata` associated with the `Table` to which the
                                  `Mapper` is mapped for a bind.

        :param ClauseElement | str clause: a raw string query or a `ClauseElement`
                                           (i.e. `~.sql.expression.select`,
                                           `~.sql.expression.text`, etc.). if the
                                           `Mapper` argument is not present or could not
                                           produce a bind, the given expression construct
                                           will be searched for a bound element, typically
                                           a `Table` associated with `Metadata`.

        :param Engine bind: if provided, it will be returned immediately.
        :param _sa_skip_events: for internal usage.
        :param _sa_skip_for_implicit_returning: for internal usage.

        :rtype: Engine
        """

        if bind is not None:
            return bind

        if mapper is None and isinstance(clause, (str, TextClause)):
            tables = extractor_services.find_table_names(clause)
            if len(tables) > 0:
                return database_services.get_table_engine(tables[0])

        return super().get_bind(mapper, clause, bind, _sa_skip_events,
                                _sa_skip_for_implicit_returning)

    @property
    def atomic(self):
        """
        gets a value indicating that this session is atomic.

        :rtype: bool
        """

        return self._atomic
