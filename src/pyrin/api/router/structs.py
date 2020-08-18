# -*- coding: utf-8 -*-
"""
router structs module.
"""

from werkzeug.routing import Map

from pyrin.core.structs import DTO


class CoreURLMap(Map):
    """
    core url map class.

    this extends the `Map` class to add some functionalities to it.
    """

    def __init__(self, rules=None, default_subdomain="", charset="utf-8",
                 strict_slashes=True, merge_slashes=True, redirect_defaults=True,
                 converters=None, sort_parameters=False, sort_key=None,
                 encoding_errors="replace", host_matching=False):
        """
        initializes an instance of CoreURLMap.

        :param RouteBase rules: sequence of url rules for this map.

        :param str default_subdomain: the default subdomain for rules without
                                      a subdomain defined.

        :param str charset: charset of the url.
                            defaults to `utf-8` if not provided.

        :param bool strict_slashes: if a rule ends with a slash but the matched
                                    url does not, redirect to the url with a trailing slash.

        :param bool merge_slashes: merge consecutive slashes when matching or building
                                   urls. matches will redirect to the normalized url.
                                   slashes in variable parts are not merged.

        :param bool redirect_defaults: this will redirect to the default rule if it
                                       wasn't visited that way. this helps creating
                                       unique urls.

        :param dict converters: a dict of converters that adds additional converters
                                to the list of converters. if you redefine one
                                converter this will override the original one.

        :param bool sort_parameters: if set to `True` the url parameters are sorted.
                                     see `url_encode` for more details.

        :param function sort_key: the sort key function for `url_encode`.
        :param str encoding_errors: the error method to use for decoding.

        :param bool host_matching: if set to `True` it enables the host matching
                                   feature and disables the subdomain one.  if
                                   enabled the `host` parameter to rules is used
                                   instead of the `subdomain` one.
        """

        super().__init__(rules, default_subdomain, charset, strict_slashes,
                         merge_slashes, redirect_defaults, converters,
                         sort_parameters, sort_key, encoding_errors,
                         host_matching)

        # a dict containing the mapping between each url and its available routes.
        # in the form of: {str url: [RouteBase route]}
        self._routes_by_url = DTO()

    def add(self, rule_factory):
        """
        adds a new rule or factory to the map and binds it.

        requires that the route is not bound to another map.

        :param RouteBase | RuleFactory rule_factory: a route or rule factory instance.
        """

        super().add(rule_factory)

        for route in rule_factory.get_rules(self):
            self._routes_by_url.setdefault(route.rule, []).append(route)

    def remove(self, rule_factory):
        """
        removes a rule or factory from the map and unbinds it.

        requires that the rule is bounded to current map.

        :param RouteBase | RuleFactory rule_factory: a `RouteBase` or `RuleFactory`
                                                     instance to be removed from this map.

        :raises RouteIsNotBoundedError: route is not bounded error.
        :raises RouteIsNotBoundedToMapError: route is not bounded to map error.
        """

        for rule in rule_factory.get_rules(self):
            rule.unbind(self)
            self._rules.remove(rule)
            self._remove_by_endpoint(rule)
            self._remove_by_url(rule)

        self._remap = True

    def _remove_by_endpoint(self, route):
        """
        removes given route from endpoint map.

        :param RouteBase route: route instance to be removed from endpoint map.
        """

        routes = self._rules_by_endpoint.get(route.endpoint)
        if routes is None:
            routes = []
        if route in routes:
            routes.remove(route)
            self._rules_by_endpoint[route.endpoint] = routes
        if len(routes) <= 0:
            self._rules_by_endpoint.pop(route.endpoint, None)

    def _remove_by_url(self, route):
        """
        removes given route from url map.

        :param RouteBase route: route instance to be removed from url map.
        """

        routes = self._routes_by_url.get(route.rule)
        if routes is None:
            routes = []
        if route in routes:
            routes.remove(route)
            self._routes_by_url[route.rule] = routes
        if len(routes) <= 0:
            self._routes_by_url.pop(route.rule, None)

    def get_routes_by_endpoint(self, endpoint):
        """
        gets the available routes for given endpoint.

        :param str endpoint: endpoint to get its routes.

        :returns: list[RouteBase]
        :rtype: list
        """

        routes = self._rules_by_endpoint.get(endpoint)
        if routes is None:
            return []

        return routes

    def get_routes_by_url(self, url):
        """
        gets the available routes for given url.

        :param str url: url to get its routes.

        :returns: list[RouteBase]
        :rtype: list
        """

        routes = self._routes_by_url.get(url)
        if routes is None:
            return []

        return routes

    def count_routes_by_endpoint(self, endpoint):
        """
        counts routes for given endpoint.

        :param str endpoint: endpoint to count its routes.

        :rtype: int
        """

        return len(self.get_routes_by_endpoint(endpoint))

    def count_routes_by_url(self, url):
        """
        counts routes for given url.

        :param str url: url to count its routes.

        :rtype: int
        """

        return len(self.get_routes_by_url(url))
