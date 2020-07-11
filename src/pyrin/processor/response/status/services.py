# -*- coding: utf-8 -*-
"""
response status services module.
"""

from pyrin.processor.response.status import ResponseStatusPackage
from pyrin.application.services import get_component


def get_status_code(method=None, **options):
    """
    gets the corresponding status code for given http method.

    if method is not provided, it gets the status code for current request's method.

    :param str method: http method to get its corresponding status code.
    :enum method:
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'
        HEAD = 'HEAD'
        TRACE = 'TRACE'
        OPTIONS = 'OPTIONS'
        PATCH = 'PATCH'
        COPY = 'COPY'
        LINK = 'LINK'
        UNLINK = 'UNLINK'
        PURGE = 'PURGE'
        VIEW = 'VIEW'

    :keyword bool has_content: specifies that the response body has content.
                               if set to False, the status code returned will
                               be `NO_CONTENT=204` for all http methods.
                               defaults to True if not provided.

    :rtype: int
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).get_status_code(method,
                                                                               **options)


def is_client_error(status_code, **options):
    """
    gets a value indicating that given status code is a client error.

    if returns True if the provided status code is
    from `ClientErrorResponseCodeEnum` values.

    :param int status_code: status code to be checked.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as client error if it is from
                                 `ClientErrorResponseCodeEnum` values. otherwise
                                 all codes from `CLIENT_ERROR_CODE_MIN` to
                                 `CLIENT_ERROR_CODE_MAX` will be considered as
                                 client error. defaults to True if not provided.

    :rtype: bool
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).is_client_error(status_code,
                                                                               **options)


def is_server_error(status_code, **options):
    """
    gets a value indicating that given status code is a server error.

    if returns True if the provided status code is
    from `ServerErrorResponseCodeEnum` values.

    :param int status_code: status code to be checked.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as server error if it is from
                                 `ServerErrorResponseCodeEnum` values. otherwise
                                 all codes from `SERVER_ERROR_CODE_MIN` to
                                 `SERVER_ERROR_CODE_MAX` will be considered
                                 as server error. defaults to True if not provided.

    :rtype: bool
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).is_server_error(status_code,
                                                                               **options)


def is_error(status_code, **options):
    """
    gets a value indicating that given status code is a client or server error.

    if returns True if the provided status code is from
    `ClientErrorResponseCodeEnum` or `ServerErrorResponseCodeEnum` values.

    :param int status_code: status code to be checked.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as error if it is from
                                 `ClientErrorResponseCodeEnum` or
                                 `ServerErrorResponseCodeEnum` values. otherwise
                                 all codes from `CLIENT_ERROR_CODE_MIN` to
                                 `CLIENT_ERROR_CODE_MAX` or from
                                 `SERVER_ERROR_CODE_MIN` to `SERVER_ERROR_CODE_MAX`
                                 will be considered as error.
                                 defaults to True if not provided.

    :rtype: bool
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).is_error(status_code,
                                                                        **options)


def is_information(status_code, **options):
    """
    gets a value indicating that given status code is a information code.

    if returns True if the provided status code is
    from `InformationResponseCodeEnum` values.

    :param int status_code: status code to be checked.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as information if it is from
                                 `InformationResponseCodeEnum` values. otherwise
                                 all codes from `INFORMATION_CODE_MIN` to
                                 `INFORMATION_CODE_MAX` will be considered as
                                 information. defaults to True if not provided.

    :rtype: bool
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).is_information(status_code,
                                                                              **options)


def is_success(status_code, **options):
    """
    gets a value indicating that given status code is a success code.

    if returns True if the provided status code is
    from `SuccessfulResponseCodeEnum` values.

    :param int status_code: status code to be checked.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as success if it is from
                                 `SuccessfulResponseCodeEnum` values. otherwise
                                 all codes from `SUCCESS_CODE_MIN` to
                                 `SUCCESS_CODE_MAX` will be considered as success.
                                 defaults to True if not provided.

    :rtype: bool
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).is_success(status_code,
                                                                          **options)


def is_redirection(status_code, **options):
    """
    gets a value indicating that given status code is a redirection code.

    if returns True if the provided status code is
    from `RedirectionResponseCodeEnum` values.

    :param int status_code: status code to be checked.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as redirection if it is from
                                 `RedirectionResponseCodeEnum` values. otherwise
                                 all codes from `REDIRECTION_CODE_MIN` to
                                 `REDIRECTION_CODE_MAX` will be considered
                                 as redirection. defaults to True if not provided.

    :rtype: bool
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).is_redirection(status_code,
                                                                              **options)


def is_processed(status_code, **options):
    """
    gets a value indicating that given status code is a processed code.

    processed codes are information or success or redirection code.
    if returns True if the provided status code is
    from `InformationResponseCodeEnum` or `SuccessfulResponseCodeEnum`
    or `RedirectionResponseCodeEnum` values.

    :param int status_code: status code to be checked.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as processed if it is from
                                 `InformationResponseCodeEnum` or
                                 `SuccessfulResponseCodeEnum` or
                                 `RedirectionResponseCodeEnum` values. otherwise
                                 all codes from `INFORMATION_CODE_MIN`
                                 to `INFORMATION_CODE_MAX` or from
                                 `SUCCESS_CODE_MIN` to `SUCCESS_CODE_MAX`
                                 or from `REDIRECTION_CODE_MIN` to
                                 `REDIRECTION_CODE_MAX` will be considered
                                 as processed. defaults to True if not provided.

    :rtype: bool
    """

    return get_component(ResponseStatusPackage.COMPONENT_NAME).is_processed(status_code,
                                                                            **options)
