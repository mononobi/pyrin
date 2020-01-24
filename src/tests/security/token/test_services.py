# -*- coding: utf-8 -*-
"""
token test_services module.
"""

import pytest

import pyrin.security.token.services as token_services
import pyrin.configuration.services as config_services

from pyrin.core.context import DTO
from pyrin.security.token.handlers.rs256 import RS256Token
from pyrin.security.token.handlers.hs256 import HS256Token
from pyrin.security.token.exceptions import DuplicatedTokenHandlerError, \
    DuplicatedTokenKidHeaderError, InvalidTokenHandlerTypeError, TokenHandlerNotFoundError, \
    TokenDecodingError

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

    token = token_services.generate_access_token(DTO())
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

    token = token_services.generate_refresh_token(DTO())
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

    with pytest.raises(TokenDecodingError):
        token_services.get_payload('invalid.fake.token')


def test_get_unverified_payload_access():
    """
    decodes an access token and gets the payload data without verifying the signature.
    """

    token = token_services.generate_access_token(DTO())
    payload_data = token_services.get_unverified_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert all(name in header_data for name in ['kid', 'alg', 'typ'])
    assert all(name in payload_data for name in ['jti', 'iat', 'type', 'exp', 'is_fresh'])


def test_get_unverified_payload_refresh():
    """
    decodes a refresh token and gets the payload data without verifying the signature.
    """

    token = token_services.generate_refresh_token(DTO())
    payload_data = token_services.get_unverified_payload(token)
    header_data = token_services.get_unverified_header(token)
    assert token is not None
    assert payload_data is not None
    assert header_data is not None
    assert all(name in header_data for name in ['kid', 'alg', 'typ'])
    assert all(name in payload_data for name in ['jti', 'iat', 'type', 'exp', 'is_fresh'])


def test_get_unverified_payload_invalid():
    """
    decodes an invalid token. it should raise an error.
    """

    with pytest.raises(TokenDecodingError):
        token_services.get_unverified_payload('invalid.fake.token')


def test_get_unverified_header():
    """
    gets the header dict of token without verifying the signature.
    """

    headers = DTO(title='header title', id=20)
    token = token_services.generate_access_token(DTO(), custom_headers=headers)
    header_data = token_services.get_unverified_header(token)
    assert all(name in header_data for name in ['kid', 'alg', 'typ', 'title', 'id'])
    assert header_data.get('title') == headers.get('title')
    assert header_data.get('id') == headers.get('id')


def test_get_unverified_header_invalid():
    """
    gets the header dict of an invalid token. it should raise an error.
    """

    with pytest.raises(TokenDecodingError):
        token_services.get_unverified_header('invalid.fake.token')


def test_generate_key_rs256():
    """
    generates a valid key for rs256 handler and returns it.
    """

    public_key, private_key = token_services.generate_key('RS256')
    assert public_key is not None and private_key is not None


def test_generate_key_hs256():
    """
    generates a valid key for hs256 handler and returns it.
    """

    key = token_services.generate_key('HS256')
    assert key is not None


def test_generate_key_invalid_handler():
    """
    generates a key for an invalid handler. it should raise an error.
    """

    with pytest.raises(TokenHandlerNotFoundError):
        token_services.generate_key('missing_handler')


def test_token_is_singleton():
    """
    tests that different types of tokens are singleton.
    """

    token1 = RS256Token()
    token2 = RS256Token()

    assert token1 == token2

    token3 = HS256Token()
    token4 = HS256Token()

    assert token3 == token4
