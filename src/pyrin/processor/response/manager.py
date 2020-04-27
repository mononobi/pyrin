# -*- coding: utf-8 -*-
"""
response manager module.
"""

from flask import make_response as flask_response

from pyrin.core.enumerations import ServerErrorResponseCodeEnum
from pyrin.settings.static import DEFAULT_STATUS_CODE
from pyrin.core.structs import Manager


class ResponseManager(Manager):
    """
    response manager class.
    """

    def _render_body(self, **options):
        """
        renders the given keyword arguments as response body.

        this method renders the given arguments as dict for json serialization.
        it simply returns the input dict as result.
        but if you want to render body to other formats, for example html,
        you could override this method and render the body as you need.

        :param object options: all keyword arguments that
                               must be rendered as response body.

        :rtype: dict
        """

        return options

    def make_response(self, **options):
        """
        makes a response from given inputs.

        note that every other keyword argument that is present
        in given input, will be passed to generated response.

        :keyword int code: response code.
                           defaults to `DEFAULT_STATUS_CODE`
                           code, if not provided.

        :keyword dict headers: headers to add into response.

        :rtype: CoreResponse
        """

        code = options.get('code', None)
        if code is None:
            code = DEFAULT_STATUS_CODE
            options.update(code=code)

        headers = options.pop('headers', None)
        if headers is None:
            headers = {}

        response = self._render_body(**options), code, headers
        return flask_response(response)

    def make_error_response(self, message, **options):
        """
        makes an error response from given inputs.

        :param str message: error message.

        :keyword int code: error code.
                           defaults to `INTERNAL_SERVER_ERROR`
                           code, if not provided.

        :keyword dict headers: headers to add into response.

        :rtype: CoreResponse
        """

        code = options.get('code', None)
        if code is None:
            code = ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR
            options.update(code=code)
        options.update(message=message)

        return self.make_response(**options)

    def make_exception_response(self, exception, **options):
        """
        makes an error response from given exception.

        if the exception does not have code, defaults
        to `INTERNAL_SERVER_ERROR` code.

        :param Exception exception: exception instance.

        :keyword int code: error code.
                           tries to get it from exception itself, if not
                           provided. defaults to `INTERNAL_SERVER_ERROR`
                           code if not available in exception.

        :keyword dict headers: headers to add into response.

        :rtype: CoreResponse
        """

        message = getattr(exception, 'description', str(exception))
        code = options.get('code', None)
        if code is None:
            code = getattr(exception, 'code',
                           ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR)
            options.update(code=code)

        return self.make_error_response(message, **options)
