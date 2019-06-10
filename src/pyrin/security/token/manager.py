# -*- coding: utf-8 -*-
"""
token manager module.
"""

import jwt

from pyrin.core.context import CoreObject, Context
from pyrin.security.token.exceptions import InvalidTokenHandlerTypeError, \
    DuplicatedTokenHandlerError, TokenHandlerNotFoundError, InvalidTokenHandlerNameError, \
    TokenKidHeaderNotSpecifiedError, TokenKidHeaderNotFoundError, DuplicatedTokenKidHeaderError
from pyrin.security.token.handlers.base import TokenBase
from pyrin.utils.custom_print import print_warning


class TokenManager(CoreObject):
    """
    token manager class.
    """

    def __init__(self):
        """
        initializes an instance of TokenManager.
        """

        CoreObject.__init__(self)

        self._token_handlers = Context()

        # a dictionary containing the relation between each kid to the handler name.
        # in the form of: {str kid: str handler_name}
        self._kid_to_handler_map = {}

    def register_token_handler(self, instance, **options):
        """
        registers a new token handler or replaces the existing one
        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's name is already available
        in registered handlers.

        :param TokenBase instance: token handler to be registered.
                                   it must be an instance of TokenBase.

        :keyword bool replace: specifies that if there is another registered
                               handler with the same name, replace it with
                               the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidTokenHandlerTypeError: invalid token handler type error.
        :raises InvalidTokenHandlerNameError: invalid token handler name error.
        :raises DuplicatedTokenHandlerError: duplicated token handler error.
        :raises DuplicatedTokenKidHeaderError: duplicated token kid header error.
        """

        if not isinstance(instance, TokenBase):
            raise InvalidTokenHandlerTypeError('Input parameter [{instance}] is '
                                               'not an instance of TokenBase.'
                                               .format(instance=str(instance)))

        if instance.get_name() is None or len(instance.get_name().strip()) == 0:
            raise InvalidTokenHandlerNameError('Token handler [{instance}] has invalid name.'
                                               .format(instance=str(instance)))

        # checking whether is there any registered instance with the same name.
        if instance.get_name() in self._token_handlers.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicatedTokenHandlerError('There is another registered token handler '
                                                  'with name [{name}] but "replace" option is '
                                                  'not set, so handler [{instance}] '
                                                  'could not be registered.'
                                                  .format(name=instance.get_name(),
                                                          instance=str(instance)))

            old_instance = self._token_handlers[instance.get_name()]
            print_warning('Token handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(instance)))

        # checking whether is there any registered instance with the same kid header.
        if instance.get_kid() in self._kid_to_handler_map.keys():
            raise DuplicatedTokenKidHeaderError('There is another registered token handler '
                                                'with "kid" header [{kid}]. each handler '
                                                'must have a unique "kid" header.'
                                                .format(kid=instance.get_kid()))

        # registering new token handler and it's mapping.
        self._token_handlers[instance.get_name()] = instance
        self._kid_to_handler_map[instance.get_kid()] = instance.get_name()

    def _get_token_handler(self, name, **options):
        """
        gets the specified token handler.

        :param str name: name of token handler to get.

        :raises TokenHandlerNotFoundError: token handler not found error.

        :rtype: TokenBase
        """

        if name not in self._token_handlers.keys():
            raise TokenHandlerNotFoundError('Token handler [{name}] not found.'
                                            .format(name=name))

        return self._token_handlers[name]

    def generate_access_token(self, handler_name, payload, **options):
        """
        generates an access token using specified handler from the given inputs and returns it.
        the generated token is in the form of `header_hash.payload_hash.signature_hash`
        and each part is encoded using a signing key.

        :param str handler_name: token handler name to be used.

        :param dict payload: a dictionary containing key/values as payload.
                             note that for better performance, keep payload
                             as small as possible.

        :keyword dict custom_headers: a dictionary containing custom headers.

        :keyword bool is_fresh: indicates that this token is fresh.
                                being fresh means that token is generated by
                                providing user credentials to server.
                                if not provided, defaults to False.

        :raises TokenHandlerNotFoundError: token handler not found error.

        :returns: token.

        :rtype: str
        """

        return self._get_token_handler(handler_name).generate_access_token(payload, **options)

    def generate_refresh_token(self, handler_name, payload, **options):
        """
        generates a refresh token using specified handler from the given inputs and returns it.
        the generated token is in the form of `header_hash.payload_hash.signature_hash`
        and each part is encoded using a signing key.

        :param str handler_name: token handler name to be used.

        :param dict payload: a dictionary containing key/values as payload.
                             note that for better performance, keep payload
                             as small as possible.

        :keyword dict custom_headers: a dictionary containing custom headers.

        :keyword bool is_fresh: indicates that this token is fresh.
                                being fresh means that token is generated by
                                providing user credentials to server.
                                if not provided, defaults to False.

        :raises TokenHandlerNotFoundError: token handler not found error.

        :returns: token.

        :rtype: str
        """

        return self._get_token_handler(handler_name).generate_refresh_token(payload, **options)

    def get_payload(self, token, **options):
        """
        decodes token using correct handler and gets the payload data.

        :param str token: token to get it's payload.

        :raises TokenKidHeaderNotSpecifiedError: token kid header not specified error.
        :raises TokenKidHeaderNotFoundError: token kid header not found error.
        :raises TokenHandlerNotFoundError: token handler not found error.

        :rtype: dict
        """

        handler_name = self._get_handler_name(token)
        return self._get_token_handler(handler_name).get_payload(token, **options)

    def get_unverified_header(self, token):
        """
        gets the header dict of token without verifying the signature.
        note that the returned header must not be trusted for critical operations.

        :param str token: token to get it's header.

        :rtype: dict
        """

        return jwt.get_unverified_header(token)

    def generate_key(self, handler_name, **options):
        """
        generates a valid key for the given handler and returns it.

        :param str handler_name: token handler name to be used.

        :keyword int length: the length of generated key in bytes.
                             note that some token handlers may not accept custom
                             key length so this value would be ignored on those handlers.

        :rtype: Union[str, tuple(str, str)]
        """

        return self._get_token_handler(handler_name).generate_key(**options)

    def _get_handler_name(self, token):
        """
        gets the handler name for specified token using the kid header.

        :param str token: token to get it's handler name.

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
