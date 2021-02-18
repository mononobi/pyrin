# -*- coding: utf-8 -*-
"""
orm session base module.
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import TextClause

import pyrin.database.services as database_services
import pyrin.database.orm.sql.extractor.services as extractor_services

from pyrin.core.globals import _
from pyrin.database.exceptions import InvalidDatabaseBindError
from pyrin.database.orm.session.exceptions import TransientSQLExpressionRequiredError


class CoreSession(Session):
    """
    core session class.

    all application sessions must be an instance this.
    """

    # these keywords are forbidden when 'execute' method is called
    # with 'transient=True' and a raw sql is given.
    NON_TRANSIENT_KEYWORDS = ['commit', 'flush', 'rollback', 'alter ', 'create ', 'drop ']

    def execute(self, clause, params=None, mapper=None, bind=None, **kw):
        """
        executes a sql expression construct or string statement.

        it will be executed within the current transaction.
        the current transaction will be resolved using the given
        entity class or object or bind name.

        this method is a wrapper for `sqlalchemy.orm.session.execute()` method
        which wraps it to bind to correct engine on different situations.
        for full documentation see the `sqlalchemy.orm.session.execute()` docs.

        :param Executable | str clause: an executable statement `Executable`
                                        expression such as `expression.select`
                                        or string sql statement to be executed.

        :param dict | list[dict] params: optional dictionary, or list of
                                         dictionaries, containing bound
                                         parameter values. if a single dictionary,
                                         single-row execution occurs. if a list of
                                         dictionaries, an `executemany' will be invoked.
                                         the keys in each dictionary must correspond
                                         to parameter names present in the statement.

        :param BaseEntity mapper: entity class or object which the given clause
                                  must be executed on its related engine.
                                  this argument takes precedence over
                                  `clause` when locating a bind.

        :param Engine bind: optional engine to be used as the bind. if
                            this engine is already involved in an ongoing transaction,
                            that connection will be used. this argument takes
                            precedence over `mapper` and `clause` and `bind_name` when
                            locating a bind.

        :keyword kw: additional keyword arguments are sent to `session.get_bind()`
                     to allow extensibility of `bind` schemes.

        :keyword str bind_name: database bind name from `database.binds.ini`
                                file on which given clause must be executed.
                                this keyword argument precedence over `mapper` and
                                `clause` when locating a bind.

        :keyword bool transient: specifies that raw sql expressions must not affect
                                 the database. if set to True and a raw sql is
                                 given, it could not contain `NON_TRANSIENT_KEYWORDS`.
                                 defaults to False if not provided.

        :raises InvalidDatabaseBindError: invalid database bind error.
        :raises TransientSQLExpressionRequiredError: transient sql expression required error.

        :returns: results of the statement execution.
        :rtype: ResultProxy
        """

        bind_name = kw.pop('bind_name', None)
        if bind is None and bind_name is not None:
            bind = database_services.get_bounded_engines().get(bind_name, None)
            if bind is None:
                raise InvalidDatabaseBindError('Database bind name [{bind_name}] '
                                               'is not available in database.binds '
                                               'config store.'
                                               .format(bind_name=bind_name))

        transient = kw.pop('transient', False)
        if transient is True and isinstance(clause, (str, TextClause)):
            raw_sql = None
            if isinstance(clause, TextClause):
                raw_sql = clause.text.lower()
            else:
                raw_sql = clause.lower()

            for item in self.NON_TRANSIENT_KEYWORDS:
                if item in raw_sql:
                    raise TransientSQLExpressionRequiredError(_('Transient sql expressions '
                                                                'should not contain [{keyword}] '
                                                                'keyword.')
                                                              .format(keyword=item.strip()))

        return super().execute(clause, params, mapper, bind, **kw)

    def get_bind(self, mapper=None, clause=None, **kw):
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

        :rtype: Engine
        """

        if mapper is None and isinstance(clause, (str, TextClause)):
            tables = extractor_services.find_table_names(clause)
            if len(tables) > 0:
                return database_services.get_table_engine(tables[0])

        return super().get_bind(mapper, clause=clause)
