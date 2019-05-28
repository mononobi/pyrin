# -*- coding: utf-8 -*-
"""
application context module.
"""

from flask import Request, Response, jsonify

from pyrin.application.exceptions import ComponentAttributeError
from pyrin.core.context import Context
from pyrin.core.exceptions import ContextAttributeError
from pyrin.settings.static import DEFAULT_STATUS_CODE, JSONIFY_MIMETYPE, \
    APPLICATION_ENCODING


class ApplicationContext(Context):
    """
    context class to hold application contextual data.
    """

    def _raise_key_error(self, key):
        """
        raises an error for given key.

        :param object key: key object that caused the error.

        :raises ContextAttributeError: context attribute error.
        """

        raise ContextAttributeError('Property [{name}] not found in application context.'
                                    .format(name=key))


class ApplicationComponent(ApplicationContext):
    """
    context class to hold application components.
    """

    def _raise_key_error(self, key):
        """
        raises an error for given key.

        :param object key: key object that caused the error.

        :raises ComponentAttributeError: component attribute error.
        """

        raise ComponentAttributeError('Component [{name}] is not available '
                                      'in application components.'.format(name=key))


class CoreResponse(Response):
    """
    represents base response.
    this class should be used as server response.
    """

    # charset of the response.
    charset = APPLICATION_ENCODING

    # default status if none is provided.
    default_status = DEFAULT_STATUS_CODE

    # default mimetype if none is provided.
    default_mimetype = JSONIFY_MIMETYPE

    # function to use as response converter.
    response_converter = jsonify

    def __init__(self, response=None, **kwargs):
        super(CoreResponse, self).__init__(response, **kwargs)

    @classmethod
    def force_type(cls, response, environ=None):
        response = cls.response_converter(response)
        return super(CoreResponse, cls).force_type(response, environ)


class CoreRequest(Request):
    """
    represents base request class.
    this class should be used for server request.
    """

    # charset of the request.
    charset = APPLICATION_ENCODING

    def __init__(self, environ, populate_request=True, shallow=False):
        super(CoreRequest, self).__init__(environ, populate_request, shallow)
