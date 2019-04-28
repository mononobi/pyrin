# -*- coding: utf-8 -*-
"""
router context module.
"""

from bshop.core.context import CoreObject


class Route(CoreObject):
    """
    Route class.
    This class should be used to manage application api routes.
    """

    def __init__(self, url, function, http_methods, **option):
        """
        Initializes a new instance of this class.

        :param str url: unique url to register this command for.
                        commands with duplicated urls will be overridden.

        :param tuple(str) http_methods: http methods that this command could handle.
                                        if not provided, default to `GET` and `HEAD`
                                        and `OPTIONS`.

        :keyword str endpoint: the endpoint for the registered URL rule. Flask
                               itself assumes the name of the view function as
                               endpoint.
        :keyword tuple(PermissionBase) permissions: list of all required permission
                                                    to execute this command.
        :keyword bool login_required: specifies that this command could not be executed
                                      if the requester has not a valid token.
                                      defaults to True if not provided.


        """

        CoreObject.__init__(self)
