# -*- coding: utf-8 -*-
"""
authentication services module.
"""

from pyrin.application.services import get_component
from pyrin.security.authentication import AuthenticationPackage


def get_relevant_authenticator_name(url):
    """
    gets the relevant authenticator name for given url rule.

    it looks for relevant authenticator in the following order:

    1. looking for it in rule based authenticators.
    2. getting default authenticator for it.

    it may return None if no relevant authenticator could be found.

    :param str url: url rule to find a relevant authenticator for it.

    :rtype: str
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME)\
        .get_relevant_authenticator_name(url)


def get_current_authenticator_name():
    """
    gets the authenticator name for current request from its matched url rule.

    it may return None if the current request does not match any url rule.
    it also returns None for routes which have `authenticated=False` in their
    definition.

    :rtype: str
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).get_current_authenticator_name()


def get_current_authenticator():
    """
    gets the authenticator for current request from its matched url rule.

    it may return None if the current request does not match any url rule.
    it also returns None for routes which have `authenticated=False` in their
    definition.

    :rtype: AbstractAuthenticatorBase
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).get_current_authenticator()


def get_rule_based_authenticator_name(url):
    """
    gets the relevant authenticator name to the given url rule.

    it may return None if no matching rule is found.

    :param str url: url to get its matching authenticator name.

    :rtype: str
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME)\
        .get_rule_based_authenticator_name(url)


def authenticator_exists(name):
    """
    gets a value indicating that an authenticator with given name exists.

    :param str name: authenticator name.

    :rtype: bool
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).authenticator_exists(name)


def get_authenticator(name, **options):
    """
    gets the authenticator with given name.

    :keyword str name: authenticator name.

    :raises AuthenticatorNotFoundError: authenticator not found error.

    :rtype: AbstractAuthenticatorBase
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).get_authenticator(name, **options)


def register_authenticator(instance, **options):
    """
    registers a new authenticator or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding an authenticator which is already registered.

    :param AbstractAuthenticatorBase instance: authenticator to be registered.
                                               it must be an instance of
                                               AbstractAuthenticatorBase.

    :keyword bool replace: specifies that if there is another registered
                           authenticator with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidAuthenticatorTypeError: invalid authenticator type error.
    :raises DuplicatedAuthenticatorError: duplicated authenticator error.
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).register_authenticator(instance,
                                                                                      **options)


def validate_authenticators():
    """
    validates that all protected routes authenticators are present.

    :raises AuthenticatorNotFoundError: authenticator not found error.
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).validate_authenticators()


def authenticate(request, **options):
    """
    authenticates given request and pushes the authenticated data into current request.

    if authentication fails, authenticated data will not be pushed into current request.

    :param CoreRequest request: request to be authenticated.

    :keyword str authenticator: authenticator name to be used. if not
                                provided, current request authenticator
                                will be used. if current request does
                                not have an authenticator, nothing will
                                be done.

    :raises AuthenticationFailedError: authentication failed error.
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).authenticate(request,
                                                                            **options)


def login(username, password, authenticator, **options):
    """
    logs in a user with given info using provided authenticator.

    it may return the required credentials if they must be returned to client.

    :param str username: username.
    :param str password: password.
    :param str authenticator: authenticator name to be used.

    :raises ValidationError: validation error.
    :raises AuthenticatorNotFoundError: authenticator not found error.

    :returns: required credentials.
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).login(username, password,
                                                                     authenticator, **options)


def logout(authenticator, **options):
    """
    logouts the current user and clears its relevant credentials.

    :param str authenticator: authenticator name to be used.

    :raises AuthenticatorNotFoundError: authenticator not found error.
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).logout(authenticator, **options)
