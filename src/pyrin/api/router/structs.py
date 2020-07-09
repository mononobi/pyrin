# -*- coding: utf-8 -*-
"""
router structs module.
"""

from werkzeug.routing import Map


class CoreURLMap(Map):
    """
    core url map class.

    this extends the `Map` class to add some functionality to it.
    """

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

            available_by_endpoint = self._rules_by_endpoint.get(rule.endpoint, None)
            if available_by_endpoint is None:
                available_by_endpoint = []
            if rule in available_by_endpoint:
                available_by_endpoint.remove(rule)
                self._rules_by_endpoint[rule.endpoint] = available_by_endpoint
            if len(available_by_endpoint) <= 0:
                self._rules_by_endpoint.pop(rule.endpoint, None)

        self._remap = True
