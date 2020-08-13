# -*- coding: utf-8 -*-
"""
token manager module.
"""

import jwt

import pyrin.configuration.services as config_services

from pyrin.core.structs import Context, DTO, Manager
from pyrin.security.token import TokenPackage
from pyrin.security.token.interface import AbstractTokenBase
from pyrin.utils.custom_print import print_warning
from pyrin.security.token.exceptions import InvalidTokenHandlerTypeError, \
    DuplicatedTokenHandlerError, TokenHandlerNotFoundError, InvalidTokenHandlerNameError, \
    TokenKidHeaderNotSpecifiedError, TokenKidHeaderNotFoundError, DuplicatedTokenKidHeaderError, \
    TokenDecodingError


class TokenManager(Manager):
    """
    token manager class.
    """

    package_class = TokenPackage

    def __init__(self):
        """
        initializes an instance of TokenManager.
        """

        super().__init__()

        self._token_handlers = Context()

        # a dictionary containing the relation between each kid to the handler name.
        # in the form of: {str kid: str handler_name}
        self._kid_to_handler_map = DTO()

    def register_token_handler(self, instance, **options):
        """
        registers a new token handler or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's name is already available
        in registered handlers.

        :param AbstractTokenBase instance: token handler to be registered.
                                           it must be an instance of AbstractTokenBase.

        :keyword bool replace: specifies that if there is another registered
                               handler with the same name, replace it with
                               the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidTokenHandlerTypeError: invalid token handler type error.
        :raises InvalidTokenHandlerNameError: invalid token handler name error.
        :raises DuplicatedTokenHandlerError: duplicated token handler error.
        :raises DuplicatedTokenKidHeaderError: duplicated token kid header error.
        """

        if not isinstance(instance, AbstractTokenBase):
            raise InvalidTokenHandlerTypeError('Input parameter [{instance}] is '
                                               'not an instance of [{base}].'
                                               .format(instance=instance,
                                                       base=AbstractTokenBase))

        if instance.get_name() is None or len(instance.get_name().strip()) == 0:
            raise InvalidTokenHandlerNameError('Token handler [{instance}] does '
                                               'not have a valid name.'
                                               .format(instance=instance))

        # checking whether is there any registered instance with the same name.
        if instance.get_name() in self._token_handlers.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicatedTokenHandlerError('There is another registered token handler '
                                                  'with name [{name}] but "replace" option is '
                                                  'not set, so handler [{instance}] '
                                                  'could not be registered.'
                                                  .format(name=instance.get_name(),
                                                          instance=instance))

            old_instance = self._token_handlers[instance.get_name()]
            print_warning('Token handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance, new_instance=instance))

        # checking whether is there any registered instance with the same kid header.
        if instance.get_kid() in self._kid_to_handler_map.keys():
            raise DuplicatedTokenKidHeaderError('There is another registered token handler '
                                                'with "kid" header [{kid}]. each handler '
                                                'must have a unique "kid" header.'
                                                .format(kid=instance.get_kid()))

        # registering new token handler and it's mapping.
        self._token_handlers[instance.get_name()] = instance
        self._kid_to_handler_map[instance.get_kid()] = instance.get_name()

    def _get_token_handler(self, **options):
        """
        gets the specified token handler.

        :keyword str handler_name: name of token handler to get.

        :raises TokenHandlerNotFoundError: token handler not found error.

        :rtype: AbstractTokenBase
        """

        handler_name = options.get('handler_name', self._get_default_handler_name())
        if handler_name not in self._token_handlers:
            raise TokenHandlerNotFoundError('Token handler [{name}] not found.'
                                            .format(name=handler_name))

        return self._token_handlers[handler_name]

    def generate_access_token(self, payload, **options):
        """
        generates an access token using specified handler from the given inputs and returns it.

        the generated token is in the form of `header_hash.payload_hash.signature_hash`
        and each part is encoded using a signing key.

        :param dict payload: a dictionary containing key/values as payload.
                             note that for better performance, keep payload
                             as small as possible.

        :keyword str handler_name: name of token handler to be used.
                                   if not provided, default handler
                                   from relevant configs will be used.

        :keyword dict custom_headers: a dictionary containing custom headers.

        :keyword bool is_fresh: indicates that this token is fresh.
                                being fresh means that token is generated by
                                providing user credentials to server.
                                if not provided, defaults to False.

        :raises TokenHandlerNotFoundError: token handler not found error.

        :returns: token.
        :rtype: str
        """

        return self._get_token_handler(**options).generate_access_token(payload, **options)

    def generate_refresh_token(self, payload, **options):
        """
        generates a refresh token using specified handler from the given inputs and returns it.

        the generated token is in the form of `header_hash.payload_hash.signature_hash`
        and each part is encoded using a signing key.

        :param dict payload: a dictionary containing key/values as payload.
                             note that for better performance, keep payload
                             as small as possible.

        :keyword str handler_name: name of token handler to be used.
                                   if not provided, default handler
                                   from relevant configs will be used.

        :keyword dict custom_headers: a dictionary containing custom headers.

        :raises TokenHandlerNotFoundError: token handler not found error.

        :returns: token.
        :rtype: str
        """

        return self._get_token_handler(**options).generate_refresh_token(payload, **options)

    def get_payload(self, token, **options):
        """
        decodes token using correct handler and gets the payload data.

        :param str token: token to get it's payload.

        :raises TokenKidHeaderNotSpecifiedError: token kid header not specified error.
        :raises TokenKidHeaderNotFoundError: token kid header not found error.
        :raises TokenHandlerNotFoundError: token handler not found error.
        :raises TokenVerificationError: token verification error.

        :rtype: dict
        """

        handler_name = self._get_handler_name(token)
        return self._get_token_handler(handler_name=handler_name).get_payload(token, **options)

    def get_unverified_payload(self, token, **options):
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

        handler_name = self._get_handler_name(token)
        return self._get_token_handler(handler_name=handler_name).get_unverified_payload(
            token, **options)

    def get_unverified_header(self, token, **options):
        """
        gets the header dict of token without verifying the signature.

        note that the returned header must not be trusted for critical operations.

        :param str token: token to get it's header.

        :raises TokenDecodingError: token decoding error.

        :rtype: dict
        """

        try:
            return jwt.get_unverified_header(token)
        except Exception as error:
            raise TokenDecodingError(error) from error

    def generate_key(self, handler_name, **options):
        """
        generates a valid key for the given handler and returns it.

        :param str handler_name: token handler name to be used.

        :keyword int length: the length of generated key in bytes.
                             note that some token handlers may not accept custom
                             key length so this value would be ignored on those handlers.

        :rtype: str | tuple[str, str]
        """

        return self._get_token_handler(handler_name=handler_name).generate_key(**options)

    def _get_handler_name(self, token):
        """
        gets the handler name for specified token using the kid header.

        :param str token: token to get it's handler name.

        :raises TokenDecodingError: token decoding error.
        :raises TokenKidHeaderNotSpecifiedError: token kid header not specified error.
        :raises TokenKidHeaderNotFoundError: token kid header not found error.

        :rtype: str
        """

        header = self.get_unverified_header(token)
        if 'kid' not in header.keys():
            raise TokenKidHeaderNotSpecifiedError('The "kid" header must be present in token.')

        kid = header['kid']
        if kid not in self._kid_to_handler_map.keys():
            raise TokenKidHeaderNotFoundError('Token kid header [{kid}] not found.'
                                              .format(kid=kid))

        return self._kid_to_handler_map[kid]

    def _get_default_handler_name(self):
        """
        gets default token handler name from configs.

        :rtype: str
        """

        return config_services.get('security', 'token', 'default_token_handler')
