# -*- coding: utf-8 -*-
"""
database request_handlers module.
"""

from sqlalchemy.exc import DatabaseError

import pyrin.database.services as database_services

from pyrin.application.decorators import after_request_handler
from pyrin.core.enumerations import ClientErrorResponseCodeEnum
from pyrin.database.exceptions import DatabaseOperationError


@after_request_handler()
def finalize_transaction(response):
    """
    this method will finalize database transaction of each request.
    we should not raise any exception in request handlers, so we return
    an error response in case of any exception.
    """

    if response.status_code >= ClientErrorResponseCodeEnum.BAD_REQUEST:
        return response

    try:
        store = database_services.get_current_store()
        session_factory = database_services.get_session_factory()
        try:
            store.commit()
            return response
        except DatabaseError as error:
            store.rollback()
            raise DatabaseOperationError(error) from error
        finally:
            session_factory.remove()
    except Exception as error:
        raise error
