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
    this method will manage all database transactions during a request lifecycle.

    :raises DatabaseOperationError: database operation error.
    """

    if response.status_code >= ClientErrorResponseCodeEnum.BAD_REQUEST:
        return response
    try:
        raise NotImplementedError('hey you')
        database_services.get_current_session().commit()
        return response
    except DatabaseError as error:
        database_services.get_current_session().rollback()
        raise DatabaseOperationError(error) from error
