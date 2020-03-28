# -*- coding: utf-8 -*-
"""
router services module.
"""

from pyrin.api.router import RouterPackage
from pyrin.application.decorators import route_factory
from pyrin.application.services import get_component


@route_factory()
def create_route(rule, **options):
    """
    creates the appropriate route based on the input parameters.

    :param str rule: unique url rule to register this route for.
                     routes with duplicated urls will be overwritten
                     if `replace=True` option is provided, otherwise an error
                     will be raised.

    :keyword tuple[str] methods: http methods that this route could handle.
                                 if not provided, defaults to `GET`, `HEAD`
                                 and `OPTIONS`.

    :keyword callable view_function: a function to be called on accessing this route.

    :keyword str endpoint: the endpoint for the registered url rule. pyrin
                           itself assumes the url rule as endpoint if not provided.

    :keyword bool login_required: specifies that this route could not be accessed
                                  if the requester has not a valid token.
                                  defaults to True if not provided.

    :keyword bool fresh_token: specifies that this route could not be accessed
                               if the requester has not a valid fresh token.
                               fresh token means a token that has been created by
                               providing user credentials to server.
                               defaults to False if not provided.

    :keyword tuple[PermissionBase] permissions: tuple of all required permissions
                                                to access this route's resource.

    :keyword int max_content_length: max content length that this route could handle,
                                     in bytes. if not provided, it will be set to
                                     `restricted_max_content_length` api config key.
                                     note that this value should be lesser than or equal
                                     to `max_content_length` api config key, otherwise
                                     it will cause an error.

    :keyword ResultSchema result_schema: result schema to be used to filter results.

    :keyword bool exposed_only: if set to False, it returns all
                                columns of the entity as dict.
                                it will be used only for entity conversion.
                                if not provided, defaults to True.
                                this value will override the corresponding
                                value of `result_schema` if provided.

    :keyword int depth: a value indicating the depth for conversion.
                        for example if entity A has a relationship with
                        entity B and there is a list of B in A, if `depth=0`
                        is provided, then just columns of A will be available
                        in result dict, but if `depth=1` is provided, then all
                        B entities in A will also be included in the result dict.
                        actually, `depth` specifies that relationships in an
                        entity should be followed by how much depth.
                        note that, if `columns` is also provided, it is required to
                        specify relationship property names in provided columns.
                        otherwise they won't be included even if `depth` is provided.
                        defaults to `default_depth` value of database config store.
                        please be careful on increasing `depth`, it could fail
                        application if set to higher values. choose it wisely.
                        normally the maximum acceptable `depth` would be 2 or 3.
                        there is a hard limit for max valid `depth` which is set
                        in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                        `depth` value than this limit, will cause an error.
                        it will be used only for entity conversion.
                        this value will override the corresponding value of
                        `result_schema` if provided.

    :raises RouteAuthenticationMismatchError: route authentication mismatch error.

    :rtype: RouteBase
    """

    return get_component(RouterPackage.COMPONENT_NAME).create_route(rule, **options)


def add_route(url, endpoint=None, view_func=None,
              provide_automatic_options=None, **options):
    """
    connects a url rule. if a view_func is provided it will be registered with the endpoint.

    if there is another rule with the same url and `replace=True` option is provided,
    it will be replaced, otherwise an error will be raised.

    :param str url: the url rule as string.

    :param str endpoint: the endpoint for the registered url rule.
                         pyrin itself assumes the url rule as endpoint.

    :param callable view_func: the function to call when serving a request to the
                               provided endpoint.

    :param bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                           added automatically.
                                           this can also be controlled by setting the
                                           `view_func.provide_automatic_options = False`
                                           before adding the rule.

    :keyword tuple[str] methods: http methods that this rule should handle.
                                 if not provided, defaults to `GET`.

    :keyword tuple[PermissionBase] permissions: tuple of all required permissions
                                                to access this route's resource.

    :keyword bool login_required: specifies that this route could not be accessed
                                  if the requester has not a valid token.
                                  defaults to True if not provided.

    :keyword bool fresh_token: specifies that this route could not be accessed
                               if the requester has not a valid fresh token.
                               fresh token means a token that has been created by
                               providing user credentials to server.
                               defaults to False if not provided.

    :keyword bool replace: specifies that this route must replace
                           any existing route with the same url or raise
                           an error if not provided. defaults to False.

    :keyword int max_content_length: max content length that this route could handle,
                                     in bytes. if not provided, it will be set to
                                     `restricted_max_content_length` api config key.
                                     note that this value should be lesser than or equal
                                     to `max_content_length` api config key, otherwise
                                     it will cause an error.

    :keyword ResultSchema result_schema: result schema to be used to filter results.

    :keyword bool exposed_only: if set to False, it returns all
                                columns of the entity as dict.
                                it will be used only for entity conversion.
                                if not provided, defaults to True.
                                this value will override the corresponding
                                value of `result_schema` if provided.

    :keyword int depth: a value indicating the depth for conversion.
                        for example if entity A has a relationship with
                        entity B and there is a list of B in A, if `depth=0`
                        is provided, then just columns of A will be available
                        in result dict, but if `depth=1` is provided, then all
                        B entities in A will also be included in the result dict.
                        actually, `depth` specifies that relationships in an
                        entity should be followed by how much depth.
                        note that, if `columns` is also provided, it is required to
                        specify relationship property names in provided columns.
                        otherwise they won't be included even if `depth` is provided.
                        defaults to `default_depth` value of database config store.
                        please be careful on increasing `depth`, it could fail
                        application if set to higher values. choose it wisely.
                        normally the maximum acceptable `depth` would be 2 or 3.
                        there is a hard limit for max valid `depth` which is set
                        in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                        `depth` value than this limit, will cause an error.
                        it will be used only for entity conversion.
                        this value will override the corresponding value of
                        `result_schema` if provided.

    :raises DuplicateRouteURLError: duplicate route url error.
    """

    return get_component(RouterPackage.COMPONENT_NAME).add_route(url, endpoint, view_func,
                                                                 provide_automatic_options,
                                                                 **options)
