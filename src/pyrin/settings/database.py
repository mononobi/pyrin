# -*- coding: utf-8 -*-
"""
database settings.
"""

# database server ip.
DATABASE_IP = '127.0.0.1'

# database server port.
DATABASE_PORT = 5432

# database user name.
DATABASE_USER = 'postgres'

# database password.
DATABASE_PASSWORD = '123'

# database encrypted password.
DATABASE_ENCRYPTED_PASSWORD = '123'

# enable sqlalchemy query log.
SQLALCHEMY_QUERY_LOG = True

# sqlalchemy query log file.
SQLALCHEMY_QUERY_LOG_FILE = '/var/log/pyrin/sqlalchemy.log'

# database URI that should be used for the connection.
# (dialect+driver://username:password@host:port/database)
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:123@127.0.0.1:5432/pyrin_devel'

# log all the statements issued to stderr which can be useful for debugging.
SQLALCHEMY_ECHO = True

# Flask-SQLAlchemy will track modifications of objects and emit signals.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# will log all the SQL queries sent to the database until the end of request.
SQLALCHEMY_RECORD_QUERIES = True
