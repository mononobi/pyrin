# -*- coding: utf-8 -*-
"""
token handlers base module.
"""

import time

from jwt import decode, encode

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject, DTO
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utils import unique_id


class TokenHandlerBase(CoreObject):
    """
    token base handler class.
    """

    def __init__(self):
        """
        initializes an instance of TokenHandlerBase.
        """

        CoreObject.__init__(self)

    def generate_access_token(self, payload, **options):
        """
        generates an access token from given payload and parameters.
        the generated token is in the form of `header_hash.payload_hash.signature_hash`
        and each part is encoded using a signing key.

        :param dict payload: a dictionary containing key/values as payload.
                             note that for better performance, keep payload
                             as small as possible.

        :keyword dict custom_headers: a dictionary containing custom headers.

        :returns: token as bytes.

        :rtype: bytes
        """

        updated_payload = payload or {}
        updated_payload.update(**self._get_access_token_required_claims())

        return encode(updated_payload,
                      self._get_encoding_key(),
                      self._get_algorithm(),
                      options.get('custom_headers', None))

    def generate_refresh_token(self, payload, **options):
        """
        generates a refresh token from given payload and parameters.
        the generated token is in the form of `header_hash.payload_hash.signature_hash`
        and each part is encoded using a signing key.

        :param dict payload: a dictionary containing key/values as payload.
                             note that for better performance, keep payload
                             as small as possible.

        :keyword dict custom_headers: a dictionary containing custom headers.

        :returns: token as bytes.

        :rtype: bytes
        """

        updated_payload = payload or {}
        updated_payload.update(**self._get_refresh_token_required_claims())

        return encode(updated_payload,
                      self._get_encoding_key(),
                      self._get_algorithm(),
                      options.get('custom_headers', None))

    def get_payload(self, token, **options):
        """
        decodes token and gets the payload data.

        :param bytes token: token as bytes.

        :keyword str algorithm: algorithm to use for decoding the token.
                                if not provided defaults to `HS256`.

        :rtype: dict
        """

        decode(token,
               self._get_decoding_key(),
               True,
               self._get_algorithm(),
               self._get_default_options())

    def _get_common_required_claims(self):
        """
        gets a dictionary containing common required claims
        for access and refresh tokens.

        :returns: dict(str jti: jwt id,
                       int iat: issued time)

        :rtype: dict
        """

        now = time.time()

        return DTO(jti=str(unique_id.generate_uuid4()),
                   iat=now)

    def _get_access_token_required_claims(self):
        """
        gets a dictionary containing required claims for access token.

        :returns: dict(str jti: jwt id,
                       int iat: issued time,
                       int exp: expire time)

        :rtype: dict
        """

        common_required = self._get_common_required_claims()
        expire_duration = self._get_access_token_lifetime()
        expiration = common_required.iat + expire_duration
        common_required.update(exp=expiration)

        return common_required

    def _get_refresh_token_required_claims(self):
        """
        gets a dictionary containing required claims for refresh token.

        :returns: dict(str jti: jwt id,
                       int iat: issued time,
                       int exp: expire time)

        :rtype: dict
        """

        common_required = self._get_common_required_claims()
        expire_duration = self._get_refresh_token_lifetime()
        expiration = common_required.iat + expire_duration
        common_required.update(exp=expiration)

        return common_required

    def _get_default_options(self):
        """
        gets a dictionary containing default options.

        :returns: dict(bool verify_signature: verify signature,
                       bool verify_exp: verify expire time,
                       bool verify_nbf: verify not before,
                       bool verify_iat: verify issued at,
                       bool verify_aud: verify audience,
                       bool verify_iss: verify issuer,
                       bool require_exp: requires expire time,
                       bool require_iat: requires issued time,
                       bool require_nbf: requires not before time)

        :rtype: dict
        """

        return DTO(verify_signature=True,
                   verify_exp=True,
                   verify_nbf=True,
                   verify_iat=True,
                   verify_aud=True,
                   verify_iss=True,
                   require_exp=True,
                   require_iat=True,
                   require_nbf=False)

    def _get_encoding_key(self):
        """
        gets the signing key for encoding.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _get_decoding_key(self):
        """
        gets the signing key for decoding.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _get_access_token_lifetime(self):
        """
        gets access token lifetime.

        :rtype: int
        """

        return config_services.get('security', 'token', 'access_token_lifetime')

    def _get_refresh_token_lifetime(self):
        """
        gets refresh token lifetime.

        :rtype: int
        """

        return config_services.get('security', 'token', 'refresh_token_lifetime')

    def _get_algorithm(self):
        """
        gets the algorithm for signing keys.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()
