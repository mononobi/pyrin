# -*- coding: utf-8 -*-
"""
database request_handlers module.
"""

from sqlalchemy.exc import DatabaseError

import pyrin.database.services as database_services
import pyrin.logging.services as logging_services
import pyrin.security.session.services as session_services

from pyrin.application.decorators import after_request_handler
from pyrin.core.enumerations import ClientErrorResponseCodeEnum, ServerErrorResponseCodeEnum
from pyrin.database.exceptions import DatabaseOperationError
from pyrin.utils import response as response_utils


@after_request_handler()
def finalize_transaction(response):
    """
    this method will finalize database transaction of each request.
    we should not raise any exception in request handlers, so we return
    an error response in case of any exception.
    """

    client_request = None
    try:
        client_request = session_services.get_current_request()
        store = database_services.get_current_store()
        session_factory = database_services.get_session_factory()
        try:
            if response.status_code >= ClientErrorResponseCodeEnum.BAD_REQUEST:
                store.rollback()
                return response

            store.commit()
            return response
        except DatabaseError as error:
            store.rollback()
            raise DatabaseOperationError(error) from error
        finally:
            session_factory.remove()
    except Exception as error:
        logging_services.exception('{client_request} - {message}'
                                   .format(message=str(error),
                                           client_request=client_request))

        return response_utils.make_exception_response(error,
                                                      code=ServerErrorResponseCodeEnum.
                                                      INTERNAL_SERVER_ERROR)
