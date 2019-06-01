# -*- coding: utf-8 -*-
"""
token manager module.
"""

import time

from jwt import decode, encode

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject, DTO
from pyrin.utils import unique_id


class TokenManager(CoreObject):
    """
    token manager class.
    """

    def generate_token(self, payload, **options):
        """
        generates a token from given payload and parameters.
        the generated token is in the form of `header_hash.payload_hash.signature_hash`
        and each part is encoded using a secret key.

        :param dict payload: a dictionary containing key/values as payload.
                             note that for better performance, keep payload
                             as small as possible.

        :keyword str algorithm: algorithm to use for signing the token.
                                if not provided defaults to `HS256`.

        :keyword dict custom_headers: a dictionary containing custom headers.

        :returns: token as bytes.

        :rtype: bytes
        """

        updated_payload = payload or {}
        updated_payload.update(**self._get_required_claims())

        return encode(updated_payload,
                      config_services.get('security', 'token', 'token_signing_key'),
                      options.get('algorithm',
                                  config_services.get('security', 'token', 'signing_algorithm')),
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
               config_services.get('security', 'token', 'token_signing_key'),
               True,
               options.get('algorithm',
                           config_services.get('security', 'token', 'signing_algorithm')),
               self._get_default_options())

    def _get_required_claims(self):
        """
        gets a dictionary containing required claims.
        if you want to change the required claims, you could
        subclass TokenManager and override this method.

        :returns: dict(UUID jti: jwt id,
                       int iat: issued time,
                       int exp: expire time)

        :rtype: dict
        """

        now = time.time()
        expire_duration = config_services.get('security', 'token', 'access_token_lifetime')
        expiration = now + expire_duration

        return DTO(jti=unique_id.generate(),
                   iat=now,
                   exp=expiration)

    def _get_default_options(self):
        """
        gets a dictionary containing default options.
        if you want to change the default options, you could
        subclass TokenManager and override this method.

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
