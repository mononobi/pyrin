# -*- coding: utf-8 -*-
"""
authentication handlers base module.
"""

from abc import abstractmethod

import pyrin.security.token.services as token_services
import pyrin.security.session.services as session_services
import pyrin.utils.misc as misc_utils

from pyrin.core.globals import _
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.enumerations import TokenTypeEnum
from pyrin.security.authentication.interface import AbstractAuthenticatorBase
from pyrin.security.authentication.handlers.exceptions import RefreshTokenRequiredError, \
    AuthenticatorNameIsRequiredError, AccessTokenRequiredError, InvalidUserError, \
    AccessAndRefreshTokensDoesNotBelongToSameUserError, InvalidAccessTokenError, \
    InvalidTokenAuthenticatorError, InvalidRefreshTokenError, UserCredentialsRevokedError, \
    InvalidUserIdentityError, ProvidedUsernameOrPasswordAreIncorrect


class AuthenticatorBase(AbstractAuthenticatorBase):
    """
    authenticator base class.

    all application authenticators must be subclassed from this.
    """

    # each subclass must set an authenticator name in this attribute.
    _name = None

    def __init__(self, *args, **options):
        """
        initializes and instance of AuthenticatorBase.

        :raises AuthenticatorNameIsRequiredError: authenticator name is required error.
        """

        super().__init__()

        if not self._name or self._name.isspace():
            raise AuthenticatorNameIsRequiredError('Authenticator [{instance}] does not '
                                                   'have a name.'.format(instance=self))

    def _get_info(self, payload, **options):
        """
        gets the info of given payload to be set in current request.

        :param dict | str payload: credential payload.

        :rtype: dict
        """

        result = dict()
        extra_info = self._get_extra_info(payload, **options)
        if extra_info:
            result.update(extra_info)

        return result

    def _get_extra_info(self, payload, **options):
        """
        gets the info of given payload to be set in current request.

        it could be None if no extra info must be set in current request.

        :param dict | str payload: credential payload.

        :rtype: dict
        """

        return None

    def _get_user_info(self, user, **options):
        """
        gets the info of given user to be set in current request.

        it could be None if no extra info must be set in current request.

        :param BaseEntity | ROW_RESULT user: user entity to get its info.

        :rtype: object | dict
        """

        return None

    def _get_custom_component_key(self, user, *args, **options):
        """
        gets custom component key for given user if required to be set in current request.

        this method could be overridden in subclasses if required.

        :param BaseEntity | ROW_RESULT user: authenticated user entity.

        :rtype: object
        """

        return None

    def _set_custom_component_key(self, value):
        """
        sets the provided value as custom component key into current request.

        :param object value: value to be pushed as component custom key.

        :raises InvalidComponentCustomKeyError: invalid component custom key error.
        """

        session_services.set_component_custom_key(value)

    def _pre_authenticate(self, *payloads, **options):
        """
        pre-authenticates the user with given credentials.

        this method could be overridden in subclasses if pre-authentication is required.
        it must raise an `AuthenticationFailedError` if pre-authentication failed.

        :param dict | str payloads: credential payloads.
                                    it is usually an access token, refresh
                                    token or a session identifier.
                                    it can be multiple items if required.
        """
        pass

    def _authenticate(self, *payloads, **options):
        """
        authenticates the user with given credentials.

        :param dict | str payloads: credential payloads.
                                    it is usually an access token, refresh
                                    token or a session identifier.
                                    it can be multiple items if required.

        :raises UserCredentialsRevokedError: user credentials revoked error.
        :raises AuthenticationFailedError: authentication failed error.
        :raises InvalidUserError: invalid user error.
        :raises InvalidUserIdentityError: invalid user identity error.
        """

        if self._is_revoked(*payloads, **options):
            raise UserCredentialsRevokedError(_('User credentials are revoked.'))

        self._pre_authenticate(*payloads, **options)
        user_payload = self._get_user_related_payload(*payloads, **options)
        user = self._get_user(user_payload, **options)
        if not user:
            raise InvalidUserError('User could not be None.')

        identity = self._get_user_identity(user, **options)
        if not identity:
            raise InvalidUserIdentityError('User identity could not be None.')

        info = self._get_info(user_payload, **options)
        user_info = self._get_user_info(user, **options)
        if user_info:
            info.update(user_info)

        session_services.set_current_user(identity, info)
        custom_component_key = self._get_custom_component_key(user, user_payload, **options)
        if custom_component_key is not None:
            self._set_custom_component_key(custom_component_key)

    def _is_revoked(self, *payloads, **options):
        """
        gets a value indicating that given payloads are revoked.

        if you want to implement credential revocation, you must implement
        this method. otherwise it will always return False.

        :param dict | str payloads: credential payloads.
                                    it is usually an access token, refresh
                                    token or a session identifier.
                                    it can be multiple items if required.

        :rtype: bool
        """

        return False

    def _persist_payloads(self, user, *payloads, **options):
        """
        persists given payloads for user login.

        this is needed if you want to use credentials revocation.
        if you do not need this feature, you can leave this method unimplemented.

        :param BaseEntity | ROW_RESULT user: user to persist its generated credentials.

        :param dict | str payloads: credential payloads.
                                    it is usually an access token, refresh
                                    token or a session identifier.
                                    it can be multiple items if required.
        """
        pass

    def _persist_login(self, user, **options):
        """
        persists required login data for given user.

        this method is intended to be overridden in subclasses to perform
        custom actions. for example updating the last login datetime of user.

        :param BaseEntity | ROW_RESULT user: user to persist its login data.
        """
        pass

    def _generate_credentials(self, user, **options):
        """
        generates the required credentials for given user for a successful login.

        :param BaseEntity | ROW_RESULT user: user to be logged in.

        :returns: required credentials to be returned to client.
        """

        credentials = self._create_credentials(user, **options)
        credentials = misc_utils.make_iterable(credentials, tuple)
        payloads = self._get_payloads(*credentials, **options)
        payloads = misc_utils.make_iterable(payloads, tuple)
        self._persist_payloads(user, *payloads, **options)
        return self._get_client_credentials(*credentials, **options)

    def authenticate(self, request, **options):
        """
        authenticates the user for given request.

        :param CoreRequest request: current request object.

        :raises AuthenticationFailedError: authentication failed error.
        """

        credentials = self._get_credentials(request, **options)
        credentials = misc_utils.make_iterable(credentials, tuple)
        payloads = self._get_payloads(*credentials, **options)
        payloads = misc_utils.make_iterable(payloads, tuple)
        self._authenticate(*payloads, **options)

    def is_fresh(self):
        """
        gets a value indicating that current request has a fresh authentication.

        fresh authentication means an authentication which is done by providing
        user credentials to server.
        if you do not want to implement such a concept in your authenticator,
        you can leave this method unimplemented and it will always return False.

        :rtype: bool
        """

        return False

    def login(self, username, password, **options):
        """
        logs in a user with given info and stores/generates the relevant credentials.

        it may return the required credentials if they must be sent to client.

        :param str username: username.
        :param str password: password.

        :raises ProvidedUsernameOrPasswordAreIncorrect: provided username or
                                                        password are incorrect.

        :returns: required credentials to be returned to client.
        """

        user = self._get_login_user(username, password, **options)
        if user is None:
            raise ProvidedUsernameOrPasswordAreIncorrect(_('The provided username or '
                                                           'password are incorrect.'))

        self._validate_login(user, **options)
        credentials = self._generate_credentials(user, **options)
        self._persist_login(user, **options)
        return credentials

    def logout(self, **options):
        """
        logouts the current user and clears its relevant credentials.
        """

        user = session_services.get_current_user()
        credentials = self._get_credentials(session_services.get_current_request(), **options)
        credentials = misc_utils.make_iterable(credentials, tuple)
        payloads = self._get_payloads(*credentials, **options)
        payloads = misc_utils.make_iterable(payloads, tuple)
        self._revoke(user, *payloads, **options)

    @abstractmethod
    def _create_credentials(self, user, **options):
        """
        creates the required credentials for given user for a successful login.

        :param BaseEntity | ROW_RESULT user: user to be logged in.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: created credentials.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_client_credentials(self, *credentials, **options):
        """
        gets the credentials that must be returned to client.

        :param str credentials: user credentials.
                                it is usually the contents of
                                authorization or cookie headers.
                                it can be multiple items if required.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: required credentials to be returned to client.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _revoke(self, *payloads, **options):
        """
        revokes the given payloads for user logout.

        :param dict | str payloads: credential payloads.
                                    it is usually an access token, refresh
                                    token or a session identifier.
                                    it can be multiple items if required.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_login_user(self, username, password, **options):
        """
        gets the related user entity to given inputs for logging in.

        it must return None if no user found.

        :param str username: username.
        :param str password: password.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: BaseEntity | ROW_RESULT
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _validate_login(self, user, **options):
        """
        validates that given user can actually logged in.

        if user should not be logged in it must raise a relevant authorization failed error.

        :param BaseEntity | ROW_RESULT user: user to be logged in.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_payloads(self, *credentials, **options):
        """
        gets the required payloads from given credentials.

        it can return multiple items if required.

        :param str credentials: user credentials.
                                it is usually the contents of
                                authorization or cookie headers.
                                it can be multiple items if required.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: tuple[dict | str] | dict | str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_credentials(self, request, **options):
        """
        gets the required credentials from given request.

        credentials are usually the contents of authorization or cookie headers.
        it can return multiple items if required.

        :param CoreRequest request: current request object.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: tuple[str] | str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_user_related_payload(self, *payloads, **options):
        """
        gets a single value as user related payload to be used to fetch related user.

        :param dict | str payloads: credential payloads.
                                    it is usually an access token, refresh
                                    token or a session identifier.
                                    it can be multiple items if required.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict | str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_user_identity(self, user, **options):
        """
        gets the identity of given user to be set in current request.

        the identity is normally the primary key of user entity.
        but it could be a dict of multiple values if required.

        :param BaseEntity | ROW_RESULT user: user entity to get its identity.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object | dict
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_user(self, payload, **options):
        """
        gets the user entity from given inputs.

        this method must return a user on success or raise an error
        if it can not fetch related user to given payload.

        :param dict | str payload: credential payload.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: BaseEntity | ROW_RESULT
        """

        raise CoreNotImplementedError()

    @property
    def name(self):
        """
        gets the name of this authenticator.

        :rtype: str
        """

        return self._name


class TokenAuthenticatorBase(AuthenticatorBase):
    """
    token authenticator base class.

    all application token authenticators must be subclassed from this.
    """

    # header name to read access token from it.
    ACCESS_TOKEN_HOLDER = 'Authorization'

    # cookie or header name to read refresh token from it.
    REFRESH_TOKEN_HOLDER = 'Refresh-Auth'

    # a key name to hold user identity in token payloads.
    USER_IDENTITY_HOLDER = 'sub'

    # a key name to hold authenticator name in token payloads.
    AUTHENTICATOR_HOLDER = 'auth'

    # specifies that this authenticator requires refresh token.
    _refresh_token = True

    # specifies that refresh token must be read from a cookie.
    # if set to False, it will be read from a normal header.
    _refresh_token_in_cookie = True

    def _get_token_payload(self, token, **options):
        """
        gets the payload of given token.

        :param str token: token.

        :returns: tuple[dict header, dict payload]
        :rtype: tuple[dict, dict]
        """

        header = token_services.get_unverified_header(token, **options)
        payload = token_services.get_payload(token, **options)
        return header, payload

    def _get_access_token_payload(self, access_token, **options):
        """
        gets the given access token payload.

        :param str access_token: access token.

        :raises AccessTokenRequiredError: access token required error.

        :rtype: dict
        """

        if not access_token:
            raise AccessTokenRequiredError(_('Access token is required for authentication.'))

        header, payload = self._get_token_payload(access_token, **options)
        self._validate_access_token(header, payload, **options)
        return payload

    def _get_refresh_token_payload(self, refresh_token, **options):
        """
        gets the given refresh token payload.

        :param str refresh_token: refresh token.

        :raises RefreshTokenRequiredError: refresh token required error.

        :rtype: dict
        """

        if not refresh_token:
            raise RefreshTokenRequiredError(_('Refresh token is required for authentication.'))

        header, payload = self._get_token_payload(refresh_token, **options)
        self._validate_refresh_token(header, payload, **options)
        return payload

    def _get_payloads(self, access_token, refresh_token, **options):
        """
        gets the required payloads from given credentials.

        :param str access_token: access token.
        :param str refresh_token: refresh token.

        :returns: tuple[dict access_token_payload, dict refresh_token_payload]
        :rtype: tuple[dict]
        """

        access_token_payload = self._get_access_token_payload(access_token, **options)
        refresh_token_payload = None
        if self._refresh_token:
            refresh_token_payload = self._get_refresh_token_payload(refresh_token, **options)

        return access_token_payload, refresh_token_payload

    def _get_access_token_credential(self, request):
        """
        gets access token from given request.

        :param CoreRequest request: current request object.

        :rtype: str
        """

        return request.headers.get(self.ACCESS_TOKEN_HOLDER)

    def _get_refresh_token_credential(self, request):
        """
        gets refresh token from given request.

        :param CoreRequest request: current request object.

        :rtype: str
        """

        if self._refresh_token_in_cookie:
            return request.cookies.get(self.REFRESH_TOKEN_HOLDER)

        return request.headers.get(self.REFRESH_TOKEN_HOLDER)

    def _get_credentials(self, request, **options):
        """
        gets the required credentials from given request.

        credentials are usually the contents of authorization or cookie headers.
        it can return multiple items if required.

        :param CoreRequest request: current request object.

        :returns: tuple[str access_token, str refresh_token]
        :rtype: tuple[str, str]
        """

        access_token = self._get_access_token_credential(request)
        refresh_token = None
        if self._refresh_token:
            refresh_token = self._get_refresh_token_credential(request)

        return access_token, refresh_token

    def _validate_same_user(self, access_token_payload, refresh_token_payload, **options):
        """
        validates that both tokens are related to the same user.

        :param dict access_token_payload: access token payload.
        :param dict refresh_token_payload: refresh token payload.

        :raises AccessAndRefreshTokensDoesNotBelongToSameUserError: access and refresh tokens
                                                                    does not belong to same
                                                                    user error.
        """

        access_user = access_token_payload.get(self.USER_IDENTITY_HOLDER)
        refresh_user = refresh_token_payload.get(self.USER_IDENTITY_HOLDER)
        if access_user != refresh_user:
            raise AccessAndRefreshTokensDoesNotBelongToSameUserError(_('Provided access and '
                                                                       'refresh tokens does not '
                                                                       'belong to the same user.'))

    def _validate_access_token(self, header, payload, **options):
        """
        validates given header and payload of an access token.

        :param dict header: token header.
        :param dict payload: token payload.

        :raises InvalidAccessTokenError: invalid access token error.
        :raises InvalidTokenAuthenticatorError: invalid token authenticator error.
        """

        if not header or not payload or not payload.get(self.USER_IDENTITY_HOLDER) or \
                payload.get('type') != TokenTypeEnum.ACCESS:
            raise InvalidAccessTokenError(_('Provided access token is invalid.'))

        generator = payload.get(self.AUTHENTICATOR_HOLDER)
        if generator != self.name:
            raise InvalidTokenAuthenticatorError(_('This access token is generated using '
                                                   'another authenticator with name [{name}].')
                                                 .format(name=generator))

    def _validate_refresh_token(self, header, payload, **options):
        """
        validates given header and payload of a refresh token.

        :param dict header: token header.
        :param dict payload: token payload.

        :raises InvalidRefreshTokenError: invalid refresh token error.
        :raises InvalidTokenAuthenticatorError: invalid token authenticator error.
        """

        if not header or not payload or not payload.get(self.USER_IDENTITY_HOLDER) or \
                payload.get('type') != TokenTypeEnum.REFRESH:
            raise InvalidRefreshTokenError(_('Provided refresh token is invalid.'))

        generator = payload.get(self.AUTHENTICATOR_HOLDER)
        if generator != self.name:
            raise InvalidTokenAuthenticatorError(_('This refresh token is generated using '
                                                   'another authenticator with name [{name}].')
                                                 .format(name=generator))

    def _get_extra_info(self, payload, **options):
        """
        gets the info of given payload to be set in current request.

        :param dict payload: access token payload.

        :rtype: dict
        """

        return dict(is_fresh=payload.get('is_fresh') or False)

    def _pre_authenticate(self,  access_token_payload, refresh_token_payload, **options):
        """
        pre-authenticates the user with given credentials.

        :param dict access_token_payload: access token payload.
        :param dict refresh_token_payload: refresh token payload.

        :raises AccessAndRefreshTokensDoesNotBelongToSameUserError: access and refresh tokens
                                                                    does not belong to same
                                                                    user error.

        :raises UserCredentialsRevokedError: user credentials revoked error.
        """

        if self._refresh_token:
            self._validate_same_user(access_token_payload,
                                     refresh_token_payload, **options)

    def _get_user_related_payload(self, access_token_payload,
                                  refresh_token_payload, **options):
        """
        gets a single value as user related payload to be used to fetch related user.

        it simply returns the access token payload.

        :param dict access_token_payload: access token payload.
        :param dict refresh_token_payload: refresh token payload.

        :rtype: dict
        """

        return access_token_payload

    def _create_credentials(self, user, **options):
        """
        creates the required access and refresh tokens for given user for a successful login.

        :param BaseEntity | ROW_RESULT user: user to be logged in.

        :returns: tuple[str access_token, str refresh_token]
        :rtype: tuple[str, str]
        """

        access_claims = self._get_access_token_claims(user, **options) or {}
        refresh_claims = {}
        if self._refresh_token:
            refresh_claims = self._get_refresh_token_claims(user, **options) or {}

        common_claims = dict()
        common_claims[self.AUTHENTICATOR_HOLDER] = self.name
        common_claims[self.USER_IDENTITY_HOLDER] = self._get_user_identity(user, **options)
        access_claims.update(common_claims)
        if self._refresh_token:
            refresh_claims.update(common_claims)

        access_token = token_services.generate_access_token(access_claims, is_fresh=True)
        refresh_token = None
        if self._refresh_token:
            refresh_token = token_services.generate_refresh_token(refresh_claims)

        return access_token, refresh_token

    def _get_access_token_claims(self, user, **options):
        """
        gets a dict of all claims that must be added to access token payload.

        this method could be overridden in subclasses.

        :param BaseEntity | ROW_RESULT user: user to be logged in.

        :rtype: dict
        """

        return {}

    def _get_refresh_token_claims(self, user, **options):
        """
        gets a dict of all claims that must be added to refresh token payload.

        this method could be overridden in subclasses.

        :param BaseEntity | ROW_RESULT user: user to be logged in.

        :rtype: dict
        """

        return {}

    def _get_client_credentials(self, access_token, refresh_token, **options):
        """
        gets the credentials that must be returned to client.

        :param str access_token: access token.
        :param str refresh_token: refresh token.

        :returns: dict(str access_token) | dict(str access_token, str refresh_token)
        :rtype: dict
        """

        result = dict(access_token=access_token)
        if self._refresh_token:
            if self._refresh_token_in_cookie:
                session_services.set_response_cookie(self.REFRESH_TOKEN_HOLDER, refresh_token)
            else:
                result.update(refresh_token=refresh_token)

        return result

    def is_fresh(self):
        """
        gets a value indicating that current request has a fresh authentication.

        fresh authentication means an authentication which is done by providing
        user credentials to server.

        :rtype: bool
        """

        user_info = session_services.get_current_user_info()
        return user_info and user_info.get('is_fresh') is True
