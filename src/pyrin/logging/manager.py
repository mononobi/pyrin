# # -*- coding: utf-8 -*-
# """
# logging manager module.
# """
#
# import os
# import platform
# import logging
# import flask.logging
#
# from logging.handlers import SysLogHandler
#
#
# from pyrin.context import CoreObject
#
#
# class Logging(CoreObject):
#     """Configure flask logging with nice formatting and syslog support."""
#
#     def __init__(self, app=None):
#         """Boiler plate extension init with log_level being declared"""
#         self.log_level = None
#         self.app = app
#         if app is not None:
#             self.init_app(app)
#
#     def init_app(self, app):
#         """Setup the logging handlers, level and formatters.
#         Level (DEBUG, INFO, CRITICAL, etc) is determined by the
#         app.config['FLASK_LOG_LEVEL'] setting, and defaults to
#         ``None``/``logging.NOTSET``.
#         """
#         config_log_level = app.config.get('FLASK_LOG_LEVEL', None)
#
#         # Set up format for default logging
#         hostname = platform.node().split('.')[0]
#         formatter = (
#             '[%(asctime)s] %(levelname)s %(process)d [%(name)s] '
#             '%(filename)s:%(lineno)d - '
#             '[{hostname}] - %(message)s'
#         ).format(hostname=hostname)
#
#         config_log_int = None
#         set_level = None
#
#         if config_log_level:
#             config_log_int = getattr(logging, config_log_level.upper(), None)
#             if not isinstance(config_log_int, int):
#                 raise ValueError(
#                     'Invalid log level: {0}'.format(config_log_level)
#                 )
#             set_level = config_log_int
#
#         # Set to NotSet if we still aren't set yet
#         if not set_level:
#             set_level = config_log_int = logging.NOTSET
#         self.log_level = set_level
#
#         # Setup basic StreamHandler logging with format and level (do
#         # setup in case we are main, or change root logger if we aren't.
#         logging.basicConfig(format=formatter)
#         root_logger = logging.getLogger()
#         root_logger.setLevel(set_level)
#
#         # Get everything ready to setup the syslog handlers
#         address = None
#         if os.path.exists('/dev/log'):
#             address = '/dev/log'
#         elif os.path.exists('/var/run/syslog'):
#             address = '/var/run/syslog'
#         else:
#             address = ('127.0.0.1', 514)
#         # Add syslog handler before adding formatters
#         root_logger.addHandler(
#             SysLogHandler(address=address, facility=SysLogHandler.LOG_LOCAL0)
#         )
#         self.set_formatter(formatter)
#
#         return config_log_int
#
#     @staticmethod
#     def set_formatter(log_formatter):
#         """Override the default log formatter with your own."""
#         # Add our formatter to all the handlers
#         root_logger = logging.getLogger()
#         for handler in root_logger.handlers:
#             handler.setFormatter(logging.Formatter(log_formatter))