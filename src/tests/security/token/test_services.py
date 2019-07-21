# -*- coding: utf-8 -*-
"""
token test_services module.
"""

import pytest

import pyrin.security.token.services as token_services
import pyrin.configuration.services as config_services

from pyrin.core.context import DTO
from pyrin.security.token.handlers.rs256 import RS256Token
from pyrin.security.token.exceptions import DuplicatedTokenHandlerError, \
    DuplicatedTokenKidHeaderError, InvalidTokenHandlerTypeError, TokenHandlerNotFoundError, \
    TokenVerificationError

from tests.security.token.handlers.hs256_test_token import HS256TestToken


def test_register_token_handler():
    """
    registers a new token handler.
    """

    token_services.register_token_handler(HS256TestToken())


def test_register_token_handler_invalid_type():
    """
    registers an invalid token handler.
    it should raise an error.
    """

    with pytest.raises(InvalidTokenHandlerTypeError):
        token_services.register_token_handler(object())


def test_register_token_handler_duplicate():
    """
    registers an already available token handler.
    it should raise an error.
    """

    with pytest.raises(DuplicatedTokenHandlerError):
        token_services.register_token_handler(RS256Token())


def test_register_token_handler_duplicate_with_replace_duplicate_kid():
    """
    registers an already available token handler with replace
    option with duplicate kid header. it should raise an error.
    """

    with pytest.raises(DuplicatedTokenKidHeaderError):
        token_services.register_token_handler(RS256Token(), replace=True)


def test_generate_access_token_default():
    """
    generates an access token using default handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_access_token(payload, custom_headers=headers)
    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'access'
    assert payload_data.get('is_fresh') is False
    assert header_data.get('title') == headers.get('title')
    assert config_services.get('security', 'token', 'default_token_handler') == \
        header_data.get('alg')


def test_generate_access_token_default_fresh():
    """
    generates a fresh access token using default handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_access_token(payload,
                                                 custom_headers=headers,
                                                 is_fresh=True)

    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'access'
    assert payload_data.get('is_fresh') is True
    assert header_data.get('title') == headers.get('title')
    assert config_services.get('security', 'token', 'default_token_handler') == \
        header_data.get('alg')


def test_generate_access_token_default_not_fresh():
    """
    generates a not fresh access token using default handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_access_token(payload,
                                                 custom_headers=headers,
                                                 is_fresh=False)

    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'access'
    assert payload_data.get('is_fresh') is False
    assert header_data.get('title') == headers.get('title')
    assert config_services.get('security', 'token', 'default_token_handler') == \
        header_data.get('alg')


def test_generate_access_token_hs256():
    """
    generates an access token using hs256 handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_access_token(payload,
                                                 handler_name='HS256',
                                                 custom_headers=headers)

    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'access'
    assert payload_data.get('is_fresh') is False
    assert header_data.get('title') == headers.get('title')
    assert header_data.get('alg') == 'HS256'


def test_generate_access_token_rs256():
    """
    generates an access token using rs256 handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_access_token(payload,
                                                 handler_name='RS256',
                                                 custom_headers=headers)

    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'access'
    assert payload_data.get('is_fresh') is False
    assert header_data.get('title') == headers.get('title')
    assert header_data.get('alg') == 'RS256'


def test_generate_access_token_invalid_handler():
    """
    generates an access token using an invalid handler.
    it should raise an error.
    """

    with pytest.raises(TokenHandlerNotFoundError):
        payload = DTO(name='test token', value=False)
        headers = DTO(title='header title')
        token_services.generate_access_token(payload,
                                             custom_headers=headers,
                                             handler_name='missing_handler')


def test_generate_refresh_token_default():
    """
    generates a refresh token using default handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_refresh_token(payload, custom_headers=headers)
    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'refresh'
    assert payload_data.get('is_fresh') is False
    assert header_data.get('title') == headers.get('title')
    assert config_services.get('security', 'token', 'default_token_handler') == \
        header_data.get('alg')


def test_generate_refresh_token_hs256():
    """
    generates a refresh token using hs256 handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_refresh_token(payload,
                                                  handler_name='HS256',
                                                  custom_headers=headers)

    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'refresh'
    assert payload_data.get('is_fresh') is False
    assert header_data.get('title') == headers.get('title')
    assert header_data.get('alg') == 'HS256'


def test_generate_refresh_token_rs256():
    """
    generates a refresh token using rs256 handler.
    """

    payload = DTO(name='test token', value=False)
    headers = DTO(title='header title')
    token = token_services.generate_refresh_token(payload,
                                                  handler_name='RS256',
                                                  custom_headers=headers)

    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert payload_data.get('name') == payload.get('name')
    assert payload_data.get('value') == payload.get('value')
    assert payload_data.get('type') == 'refresh'
    assert payload_data.get('is_fresh') is False
    assert header_data.get('title') == headers.get('title')
    assert header_data.get('alg') == 'RS256'


def test_generate_refresh_token_invalid_handler():
    """
    generates a refresh token using an invalid handler.
    it should raise an error.
    """

    with pytest.raises(TokenHandlerNotFoundError):
        payload = DTO(name='test token', value=False)
        headers = DTO(title='header title')
        token_services.generate_refresh_token(payload,
                                              custom_headers=headers,
                                              handler_name='missing_handler')


def test_get_payload_access():
    """
    decodes access token using correct handler and gets the payload data.
    """

    token = token_services.generate_access_token({})
    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert all(name in header_data for name in ['kid', 'alg', 'typ'])
    assert all(name in payload_data for name in ['jti', 'iat', 'type', 'exp', 'is_fresh'])


def test_get_payload_refresh():
    """
    decodes refresh token using correct handler and gets the payload data.
    """

    token = token_services.generate_refresh_token({})
    payload_data = token_services.get_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert all(name in header_data for name in ['kid', 'alg', 'typ'])
    assert all(name in payload_data for name in ['jti', 'iat', 'type', 'exp', 'is_fresh'])


def test_get_payload_invalid():
    """
    decodes an invalid token. it should raise an error.
    """

    with pytest.raises(Exception):
        token_services.get_payload('invalid.fake.token')


def get_unverified_payload(token, **options):
    """
    decodes token and gets the payload data without verifying the signature.
    note that returned payload must not be trusted for any critical operations.

    :param str token: token to get it's payload.

    :raises TokenKidHeaderNotSpecifiedError: token kid header not specified error.
    :raises TokenKidHeaderNotFoundError: token kid header not found error.
    :raises TokenHandlerNotFoundError: token handler not found error.
    :raises TokenDecodingError: token decoding error.

    :rtype: dict
    """


def get_unverified_header(token, **options):
    """
    gets the header dict of token without verifying the signature.
    note that the returned header must not be trusted for critical operations.

    :param str token: token to get it's header.

    :rtype: dict
    """


def generate_key(handler_name, **options):
    """
    generates a valid key for the given handler and returns it.

    :param str handler_name: token handler name to be used.

    :keyword int length: the length of generated key in bytes.
                         note that some token handlers may not accept custom
                         key length so this value would be ignored on those handlers.

    :rtype: Union[str, tuple(str, str)]
    """
