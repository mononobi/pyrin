# -*- coding: utf-8 -*-
"""
response manager module.
"""

from werkzeug.datastructures import Headers
from flask import make_response as flask_response

from pyrin.core.enumerations import ServerErrorResponseCodeEnum
from pyrin.core.globals import ROW_RESULT
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

        data = options.get('data', None)
        if data is None:
            data = {}

        options.update(message=message, data=data)

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

    def unpack_response(self, response, **options):
        """
        unpacks the response object into a tuple of three parts.

        in the form of `(body, status_code, headers)`. if any of these
        parts are not present in provided response, it returns None for
        that specific part.

        :param tuple | object response: response object to be unpacked.

        :returns: tuple[object body, int status_code, dict headers]
        :rtype: tuple[object, int, dict]
        """

        body = None
        status_code = None
        headers = None
        if isinstance(response, tuple) and \
                not isinstance(response, ROW_RESULT) and len(response) in (2, 3):
            length = len(response)
            if length == 3:
                body, status_code, headers = response
            else:
                if isinstance(response[1], (Headers, dict, tuple, list)):
                    body, headers = response
                else:
                    body, status_code = response
        else:
            body = response

        return body, status_code, headers

    def pack_response(self, body, status_code, headers, **options):
        """
        packs the response using given values.

        it returns a tuple if status code or headers are
        not None, otherwise it just returns the body.

        :param object | CoreResponse body: body of response.
        :param int status_code: status code of response.
        :param dict headers: dict of response headers.

        :returns: tuple[object body, int status_code, dict headers] | object
        :rtype: tuple[object, int, dict] | object
        """

        if status_code is not None and headers is not None:
            return body, status_code, headers

        if status_code is not None:
            return body, status_code

        if headers is not None:
            return body, headers

        return body
