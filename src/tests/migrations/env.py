# -*- coding: utf-8 -*-
"""
alembic env module.
"""

import re
import logging

from logging.config import fileConfig

import colorama

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import pyrin.utils.unique_id as uuid_utils
import pyrin.database.migration.services as migration_services
import pyrin.globalization.datetime.services as datetime_services

from pyrin.utils.custom_print import print_colorful

from tests import PyrinTestApplication


app_instance = PyrinTestApplication(migration=True)

USE_TWOPHASE = False

# this is the alembic config object, which provides
# access to the values within the .ini file in use.
config = context.config

# interpret the config file for python logging.
# this line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# gather section names referring to different
# databases. these are named 'engine1', 'engine2'
# in the sample .ini file.
db_names = config.get_main_option('databases')

# keeps a collection of connection bind names and urls.
# default engine bind name is always default.
connection_urls = migration_services.get_connection_urls()

# add your model's 'MetaData' objects here
# for 'autogenerate' support. these must be set
# up to hold just those tables targeting a
# particular database. table.tometadata() may be
# helpful here in case a 'copy' of
# a metadata is needed.
# from myapp import mymodel
# target_metadata = {
#       'engine1':mymodel.metadata1,
#       'engine2':mymodel.metadata2
# }
target_metadata = migration_services.get_bind_name_to_metadata_map()

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option('my_important_option')
# ... etc.


def print_message(message):
    """
    prints the given message into stdout.

    :param str message: message to be printed.
    """

    print_colorful(message, colorama.Fore.CYAN, True)


def get_current_timestamp():
    """
    gets current time stamp.

    :rtype: str
    """

    current = datetime_services.now()
    return '{year}{month}{day}{hour}{minute}{second}'.format(year=current.year,
                                                             month=current.month,
                                                             day=current.day,
                                                             hour=current.hour,
                                                             minute=current.minute,
                                                             second=current.second)


def run_migrations_offline():
    """
    run migrations in 'offline' mode.

    this configures the context with just a url
    and not an engine, though an engine is acceptable
    here as well. by skipping the engine creation
    we don't even need a dbapi to be available.

    calls to context.execute() here emit the given string to the
    script output.
    """

    # for the --sql use case, run migrations for each URL into
    # individual files.

    engines = {}
    for name in re.split(r',\s*', db_names):
        # engines[name] = rec = {}
        # rec['url'] = connection_urls.get(name)
        engines[name] = rec = {}
        rec['url'] = connection_urls.get(name)
        rec['engine'] = engine_from_config(
            dict(url=connection_urls.get(name)),
            prefix="",
            poolclass=pool.NullPool,
        )

    timestamp = get_current_timestamp()
    revision = uuid_utils.generate_uuid4().hex[0:6]
    for name, rec in engines.items():
        engine = rec['engine']
        rec['connection'] = conn = engine.connect()
        print_colorful('Migrating database [{name}]'.format(name=name), True)
        file_ = 'sql/{revision}_{name}_{timestamp}.sql'.format(revision=revision,
                                                               name=name,
                                                               timestamp=timestamp)
        print_message('Writing output to [{file_name}]'.format(file_name=file_))
        with open(file_, 'w') as buffer:
            context.configure(
                url=rec['url'],
                connection=rec['connection'],
                output_buffer=buffer,
                target_metadata=target_metadata.get(name),
                literal_binds=True,
                as_sql=True,
                dialect_opts={'paramstyle': 'named'},
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def run_migrations_online():
    """
    run migrations in 'online' mode.

    in this scenario we need to create an engine
    and associate a connection with the context.
    """

    # for the direct-to-db use case, start a transaction on all
    # engines, then run all migrations, then commit all transactions.

    engines = {}
    for name in re.split(r',\s*', db_names):
        engines[name] = rec = {}
        rec['engine'] = engine_from_config(
            dict(url=connection_urls.get(name)),
            prefix="",
            poolclass=pool.NullPool,
        )

    for name, rec in engines.items():
        engine = rec['engine']
        rec['connection'] = conn = engine.connect()

        if USE_TWOPHASE:
            rec['transaction'] = conn.begin_twophase()
        else:
            rec['transaction'] = conn.begin()

    try:
        for name, rec in engines.items():
            print_message('Migrating database [{name}]'.format(name=name))
            context.configure(
                connection=rec['connection'],
                upgrade_token='%s_upgrades' % name,
                downgrade_token='%s_downgrades' % name,
                target_metadata=target_metadata.get(name),
                user_module_prefix='pyrin.database.migration.types.',
                compare_type=True,
            )
            context.run_migrations(engine_name=name)

        if USE_TWOPHASE:
            for rec in engines.values():
                rec['transaction'].prepare()

        for rec in engines.values():
            rec['transaction'].commit()

    except Exception:
        for rec in engines.values():
            rec['transaction'].rollback()
        raise
    finally:
        for rec in engines.values():
            rec['connection'].close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
