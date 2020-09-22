# -*- coding: utf-8 -*-
"""
logging test_services module.
"""

import logging

import pyrin.logging.services as logging_services

from pyrin.logging.adapters import RequestInfoLoggerAdapter


def test_reload_configs():
    """
    reloads all logging configurations from config file.
    """

    logging_services.reload_configs()


def test_get_all_loggers_initial():
    """
    checks all initial required loggers are loaded.
    """

    loggers = logging_services.get_all_loggers()
    assert all(name in loggers.keys() for name in ['sqlalchemy.engine', 'database', 'celery',
                                                   'sqlalchemy.pool', 'sqlalchemy.dialects',
                                                   'sqlalchemy.orm', 'werkzeug', 'api',
                                                   'caching.remote', 'caching.local'])


def test_get_all_loggers_packages():
    """
    checks all packages required loggers are loaded.
    """

    loggers = logging_services.get_all_loggers()
    assert all(name in loggers.keys() for name in ['api', 'database'])


def test_wrap_all_loggers():
    """
    checks that all required loggers are wrapped into an adapter.
    """

    loggers = logging_services.get_all_loggers()

    assert not any(not isinstance(logger, RequestInfoLoggerAdapter)
                   for logger in loggers.values()
                   if logging_services.should_be_wrapped(logger) is True
                   and logger.name not in ['celery.bootsteps'])

    assert any(isinstance(logger, RequestInfoLoggerAdapter) for logger in loggers.values())


def test_get_logger_existed():
    """
    gets an already existed logger.
    """

    logger = logging_services.get_logger('api')
    assert isinstance(logger, RequestInfoLoggerAdapter)


def test_get_logger_not_existed():
    """
    gets a not existed logger.
    """

    logger = logging_services.get_logger('not_existed_logger')
    assert isinstance(logger, RequestInfoLoggerAdapter)


def test_debug_root(caplog):
    """
    emits a log with debug level into root logger.
    """

    caplog.clear()
    caplog.set_level(logging.DEBUG)
    message = 'this is a debug root log.'
    logging_services.debug(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_info_root(caplog):
    """
    emits a log with info level into root logger.
    """

    caplog.clear()
    message = 'this is an info root log.'
    caplog.set_level(logging.INFO)
    logging_services.info(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_warning_root(caplog):
    """
    emits a log with warning level into root logger.
    """

    caplog.clear()
    message = 'this is a warning root log.'
    caplog.set_level(logging.WARNING)
    logging_services.warning(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_error_root(caplog):
    """
    emits a log with error level into root logger.
    """

    caplog.clear()
    message = 'this is an error root log.'
    caplog.set_level(logging.ERROR)
    logging_services.error(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_exception_root(caplog):
    """
    emits a log with error level into root logger with exception info.
    """

    message = 'this is an error with exception root log.'
    try:
        caplog.clear()
        caplog.set_level(logging.ERROR)
        raise ValueError(message)
    except ValueError as error:
        logging_services.exception(str(error))
        assert caplog.records is not None and len(caplog.records) > 0
        assert message in caplog.records[0].message
        assert caplog.records[0].exc_info is not None
        assert caplog.records[0].exc_text is not None
        assert 'ValueError' in caplog.records[0].exc_text
    finally:
        caplog.clear()


def test_critical_root(caplog):
    """
    emits a log with critical level into root logger.
    """

    caplog.clear()
    message = 'this is a critical root log.'
    caplog.set_level(logging.CRITICAL)
    logging_services.critical(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_debug_root_log_with_warning_level(caplog):
    """
    emits a log with debug level into root logger which has warning level.
    it should not be present in logs.
    """

    caplog.clear()
    message = 'this is a debug root log that should not be emitted.'
    caplog.set_level(logging.WARNING)
    logging_services.debug(message)
    assert caplog.records is None or len(caplog.records) == 0
    caplog.clear()


def test_error_root_log_with_info_level(caplog):
    """
    emits a log with error level into root logger which has info level.
    it should be present in logs.
    """

    caplog.clear()
    message = 'this is an error root log that should be emitted.'
    caplog.set_level(logging.INFO)
    logging_services.error(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_debug_new_logger(caplog):
    """
    emits a log with debug level into debug_new_logger.
    """

    caplog.clear()
    logger = logging_services.get_logger('debug_new_logger')
    caplog.set_level(logging.DEBUG, logger='debug_new_logger')
    message = 'this is a debug_new_logger log.'
    logger.debug(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_info_new_logger(caplog):
    """
    emits a log with info level into info_new_logger.
    """

    caplog.clear()
    logger = logging_services.get_logger('info_new_logger')
    caplog.set_level(logging.INFO, logger='info_new_logger')
    message = 'this is an info_new_logger log.'
    logger.info(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_warning_new_logger(caplog):
    """
    emits a log with warning level into warning_new_logger.
    """

    caplog.clear()
    logger = logging_services.get_logger('warning_new_logger')
    caplog.set_level(logging.WARNING, logger='warning_new_logger')
    message = 'this is a warning_new_logger log.'
    logger.warning(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_error_new_logger(caplog):
    """
    emits a log with error level into error_new_logger.
    """

    caplog.clear()
    logger = logging_services.get_logger('error_new_logger')
    caplog.set_level(logging.ERROR, logger='error_new_logger')
    message = 'this is an error_new_logger log.'
    logger.error(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_exception_new_logger(caplog):
    """
    emits a log with error level into exception_new_logger with exception info.
    """

    message = 'this is an error with exception_new_logger log.'
    logger = logging_services.get_logger('exception_new_logger')
    try:
        caplog.clear()
        caplog.set_level(logging.ERROR, logger='exception_new_logger')
        raise ValueError(message)
    except ValueError as error:
        logger.exception(str(error))
        assert caplog.records is not None and len(caplog.records) > 0
        assert message in caplog.records[0].message
        assert caplog.records[0].exc_info is not None
        assert caplog.records[0].exc_text is not None
        assert 'ValueError' in caplog.records[0].exc_text
    finally:
        caplog.clear()


def test_critical_new_logger(caplog):
    """
    emits a log with critical level into critical_new_logger.
    """

    caplog.clear()
    logger = logging_services.get_logger('critical_new_logger')
    caplog.set_level(logging.CRITICAL, logger='critical_new_logger')
    message = 'this is a critical_new_logger log.'
    logger.critical(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_debug_new_logger_log_with_warning_level(caplog):
    """
    emits a log with debug level into debug_to_warning_new_logger which has warning level.
    it should not be present in logs.
    """

    caplog.clear()
    message = 'this is a debug_to_warning_new_logger log that should not be emitted.'
    logger = logging_services.get_logger('debug_to_warning_new_logger')
    caplog.set_level(logging.WARNING, logger='debug_to_warning_new_logger')
    logger.debug(message)
    assert caplog.records is None or len(caplog.records) == 0
    caplog.clear()


def test_error_new_logger_log_with_info_level(caplog):
    """
    emits a log with error level into error_to_info_new_logger which has info level.
    it should be present in logs.
    """

    caplog.clear()
    message = 'this is an error_to_info_new_logger log that should be emitted.'
    logger = logging_services.get_logger('error_to_info_new_logger')
    caplog.set_level(logging.INFO, logger='error_to_info_new_logger')
    logger.error(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()


def test_error_database(caplog):
    """
    emits a log with error level into database logger.
    """

    caplog.clear()
    logger = logging_services.get_logger('database')
    message = 'this is an error database log.'
    logger.error(message)
    assert caplog.records is not None and len(caplog.records) > 0
    assert message in caplog.records[0].message
    caplog.clear()
