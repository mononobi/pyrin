# -*- coding: utf-8 -*-
"""
response status manager module.
"""

import pyrin.security.session.services as session_services

from pyrin.processor.response.status import ResponseStatusPackage
from pyrin.settings.static import DEFAULT_STATUS_CODE
from pyrin.core.structs import Manager, DTO
from pyrin.core.enumerations import SuccessfulResponseCodeEnum, HTTPMethodEnum, \
    ClientErrorResponseCodeEnum, ServerErrorResponseCodeEnum, InformationResponseCodeEnum, \
    RedirectionResponseCodeEnum


class ResponseStatusManager(Manager):
    """
    response status manager class.
    """

    # these values will be used to detect response status type from
    # status code if `strict_status=False` is passed to corresponding method.
    # if you want to provide custom non-standard response codes in your
    # application, you should override these values in a subclass.
    CLIENT_ERROR_CODE_MIN = ClientErrorResponseCodeEnum.BAD_REQUEST
    CLIENT_ERROR_CODE_MAX = 499

    SERVER_ERROR_CODE_MIN = ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR
    SERVER_ERROR_CODE_MAX = 599

    INFORMATION_CODE_MIN = InformationResponseCodeEnum.CONTINUE
    INFORMATION_CODE_MAX = 199

    SUCCESS_CODE_MIN = SuccessfulResponseCodeEnum.OK
    SUCCESS_CODE_MAX = 299

    REDIRECTION_CODE_MIN = RedirectionResponseCodeEnum.MULTIPLE_CHOICE
    REDIRECTION_CODE_MAX = 399

    package_class = ResponseStatusPackage

    def __init__(self):
        """
        initializes an instance of ResponseStatusManager.
        """

        super().__init__()

        # a dict containing the mapping between http methods and status codes.
        # in the form of: {str http_method: int status_code}
        self.__method_to_status_map = DTO()
        self.__initialize_mapping()

    def __initialize_mapping(self):
        """
        initializes the mapping between http methods and status codes.
        """

        mapping = DTO()
        mapping[HTTPMethodEnum.GET] = SuccessfulResponseCodeEnum.OK
        mapping[HTTPMethodEnum.PUT] = SuccessfulResponseCodeEnum.OK
        mapping[HTTPMethodEnum.PATCH] = SuccessfulResponseCodeEnum.OK
        mapping[HTTPMethodEnum.DELETE] = SuccessfulResponseCodeEnum.OK
        mapping[HTTPMethodEnum.POST] = SuccessfulResponseCodeEnum.CREATED

        self._customize_mapping(mapping)
        self.__method_to_status_map = mapping

    def _customize_mapping(self, mapping):
        """
        customizes the mapping between http methods and status codes.

        this method is intended to be overridden by subclasses.
        it should always do the required modifications into the input dict in-place.

        :param dict[str, int] mapping: the mapping dict.
        :note mapping: dict[str http_method: int status_code]
        """
        pass

    def get_status_code(self, method=None, **options):
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

        has_content = options.get('has_content', True)
        if has_content is False:
            return SuccessfulResponseCodeEnum.NO_CONTENT

        if method is None:
            method = session_services.get_current_request().method

        status = self.__method_to_status_map.get(method, None)
        return status or DEFAULT_STATUS_CODE

    def is_client_error(self, status_code, **options):
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

        strict_status = options.get('strict_status', True)
        if strict_status is False:
            return self.CLIENT_ERROR_CODE_MIN <= status_code <= self.CLIENT_ERROR_CODE_MAX

        return status_code in ClientErrorResponseCodeEnum.values()

    def is_server_error(self, status_code, **options):
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

        strict_status = options.get('strict_status', True)
        if strict_status is False:
            return self.SERVER_ERROR_CODE_MIN <= status_code <= self.SERVER_ERROR_CODE_MAX

        return status_code in ServerErrorResponseCodeEnum.values()

    def is_error(self, status_code, **options):
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

        return self.is_server_error(status_code, **options) or \
            self.is_client_error(status_code, **options)

    def is_information(self, status_code, **options):
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

        strict_status = options.get('strict_status', True)
        if strict_status is False:
            return self.INFORMATION_CODE_MIN <= status_code <= self.INFORMATION_CODE_MAX

        return status_code in InformationResponseCodeEnum.values()

    def is_success(self, status_code, **options):
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

        strict_status = options.get('strict_status', True)
        if strict_status is False:
            return self.SUCCESS_CODE_MIN <= status_code <= self.SUCCESS_CODE_MAX

        return status_code in SuccessfulResponseCodeEnum.values()

    def is_redirection(self, status_code, **options):
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

        strict_status = options.get('strict_status', True)
        if strict_status is False:
            return self.REDIRECTION_CODE_MIN <= status_code <= self.REDIRECTION_CODE_MAX

        return status_code in RedirectionResponseCodeEnum.values()

    def is_processed(self, status_code, **options):
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

        return self.is_success(status_code, **options) or \
            self.is_information(status_code, **options) or \
            self.is_redirection(status_code, **options)
