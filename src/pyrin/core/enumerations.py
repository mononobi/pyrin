# -*- coding: utf-8 -*-
"""
core enumerations module.
"""

import inspect

from copy import deepcopy
from collections import OrderedDict


class EnumMember:
    """
    enum member class.

    if you need localizable values for your enumerations, you could define
    enum values of this type instead of primitive types.

    for example:

    class Animal(CoreEnum):
        RABBIT = EnumMember(1, 'Rabbit')
        LION = EnumMember(2, 'Lion')
        UNKNOWN = 3

    animal_1 = Animal.RABBIT --> this returns the value of rabbit which is 1.
    animal_1_name = Animal(Animal.RABBIT) --> this returns the name of rabbit
    which is `Rabbit`.
    animal_2 = Animal.UNKNOWN --> this returns the value of unknown which is 3.
    animal_2_name = Animal(3) --> this returns the name of unknown which is `UNKNOWN`.
    animal_5 = Animal(5, silent=True) --> this returns None.
    animal_6 = Animal(6) --> this raises an attribute error.

    as you could see, you could also define enum values with primitive types if needed.
    but they won't have localizable names.
    """

    def __init__(self, value, name):
        """
        initializes an instance of EnumMember.

        :param value: enum value.
        :param str name: enum name.
        """

        self._value = value
        self._name = name

    def __str__(self):
        """
        gets the string representation of this enum member.

        :rtype: str
        """

        return self.name

    def __repr__(self):
        """
        gets the string representation of this enum member.

        :rtype: str
        """

        return '[{value}:{name}]'.format(value=self.value, name=self.name)

    def __eq__(self, other):
        """
        gets a value indicating that this enum value is equal to provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value == other.value

        return self.value == other

    def __ne__(self, other):
        """
        gets a value indicating that this enum value is not equal to provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value != other.value

        return self.value != other

    def __ge__(self, other):
        """
        implements `>=` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value >= other.value

        return self.value >= other

    def __le__(self, other):
        """
        implements `<=` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value <= other.value

        return self.value <= other

    def __gt__(self, other):
        """
        implements `>` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value > other.value

        return self.value > other

    def __lt__(self, other):
        """
        implements `<` operator to compare current enum member with provided value.

        :param EnumMember | object other: other object to be compared
                                          to this enum member.

        :rtype: bool
        """

        if isinstance(other, EnumMember):
            return self.value < other.value

        return self.value < other

    def __hash__(self):
        """
        gets the hash of this enum member.

        :rtype: int
        """

        return hash(self.value)

    @property
    def value(self):
        """
        gets this enum member's value.

        :returns: object
        """

        return self._value

    @property
    def name(self):
        """
        gets this enum member's name.

        :rtype: str
        """

        return self._name


class CoreEnumMeta(type):
    """
    core enum metaclass.
    """

    # each enum class will gain it's own attributes to save names and values of
    # it's members. the below attributes will always remain None and never get populated.
    __enum_names = None
    __enum_values = None
    __enum_dict = None

    @staticmethod
    def __new__(mcs, *args, **kwargs):
        """
        creates and returns a new class.

        note that this method will only get called once per each enum subclass.

        :rtype: type[CoreEnumMeta]
        """

        mcs._check_duplicates(args[0], args[2])
        return super().__new__(mcs, *args, **kwargs)

    def __getattribute__(cls, name):
        """
        gets an attribute of this class with given name.

        it returns the enum value, even if it is of `EnumMember` type.

        :param str name: attribute name to be get.

        :returns: object
        """

        member = type.__getattribute__(cls, name)
        # we should not call 'get_pure_value' here because it results in recursion error.
        if isinstance(member, EnumMember):
            member = member.value

        return member

    def __contains__(cls, member):
        """
        gets a value indicating that given input exists in the enumeration values.

        this method is overridden to be able to check
        for existence with `in` keyword. for example:
        has_value = 'value' in SomeEnum

        :param EnumMember | object member: value to be checked for existence.

        :rtype: bool
        """

        member = cls.get_pure_value(member)
        return member in cls.values()

    def __to_dict(cls):
        """
        gets a dict containing all values of this enum and their names.

        :returns: dict(object value, str name)
        :rtype: dict
        """

        if cls.__enum_dict is None:
            cls._populate_members()

        return cls.__enum_dict

    @staticmethod
    def _check_duplicates(enum, attrs):
        """
        checks that is there any enum members with the same value.

        if it does, it raises an error.

        :param str enum: enum name.
        :param dict attrs: all attributes of this class.

        :raise ValueError: value error.
        """

        values = []
        for name, value in attrs.items():
            if CoreEnumMeta._is_enumeration(name, value):
                pure_value = CoreEnumMeta.get_pure_value(value)
                if pure_value in values:
                    raise ValueError('Enumeration [{enum}] has multiple '
                                     'members with value [{value}].'
                                     .format(enum=enum, value=pure_value))

                values.append(pure_value)
                continue

    @staticmethod
    def _is_enumeration(name, value):
        """
        gets a value indicating that given name belongs to an enum member.

        enum members must not start or end with underscores `_`.
        callable values are also ignored.
        all `EnumMember` instances will be accepted without considering their naming style.

        :param str name: name to be checked.
        :param EnumMember | object value: value to be checked.

        :rtype: bool
        """

        if isinstance(value, EnumMember):
            return True

        if name is None or value is None or callable(value) or \
                inspect.isfunction(value) or inspect.ismethod(value) or \
                inspect.ismethoddescriptor(value) or inspect.isclass(value):
            return False

        return not name.startswith('_') and not name.endswith('_')

    @staticmethod
    def get_pure_value(member):
        """
        gets the pure value of given value.

        if the value is an instance of `EnumMember` it returns the `value` of it.
        otherwise it returns the same input.

        :param EnumMember | object member: value to get its pure value.

        :returns: object
        """

        if isinstance(member, EnumMember):
            return member.value

        return member

    def _populate_members(cls):
        """
        populates this enum's names and values and dictionary.
        """

        names = []
        values = []
        dictionary = OrderedDict()
        for name in cls.__dict__:
            item = cls.__dict__.get(name)
            if cls._is_enumeration(name, item):
                if isinstance(item, EnumMember):
                    name = item.name
                    item = item.value
                names.append(name)
                values.append(item)
                dictionary[item] = name

        cls.__enum_names = tuple(names)
        cls.__enum_values = tuple(values)
        cls.__enum_dict = dictionary

    def values(cls):
        """
        gets a tuple containing all values in the enumeration.

        :rtype: tuple
        """

        if cls.__enum_values is None:
            cls._populate_members()

        return cls.__enum_values

    def names(cls):
        """
        gets a tuple containing all names in the enumeration.

        :rtype: tuple
        """

        if cls.__enum_names is None:
            cls._populate_members()

        return cls.__enum_names

    def to_dict(cls):
        """
        gets a dict containing all values of this enum and their names.

        :returns: dict(object value, str name)
        :rtype: dict
        """

        return deepcopy(cls.__to_dict())

    def str(cls, value):
        """
        gets the name of given value in enumeration.

        note that if the value is not an `EnumMember` instance, it does not have
        a name and the name of it's attribute will be returned instead.
        if the value does not exist in enumeration, it raises an error.

        :param EnumMember | object value: value to get its name.

        :raises AttributeError: attribute error.

        :rtype: str
        """

        value = cls.get_pure_value(value)
        name = cls.__to_dict().get(value)
        if name is None:
            raise AttributeError('Enumeration [{enum}] does not have '
                                 'a member with value [{value}].'
                                 .format(enum=cls.__name__, value=value))

        return name


class CoreEnum(metaclass=CoreEnumMeta):
    """
    core enum class.

    all application enumerations must inherit from this class.
    """

    @staticmethod
    def __new__(cls, value, silent=False):
        """
        gets the name of given value in enumeration.

        note that if the value is not an `EnumMember` instance, it does not have
        a name and the name of it's attribute will be returned instead.
        if the value does not exist in enumeration, it raises an error.

        example usage:

        class CarEnum(CoreEnum):
            MERCEDES = EnumMember(1, 'Mercedes')
            BMW = 2

        name1 = CarEnum(1) --> `Mercedes`
        name2 = CarEnum(CarEnum.MERCEDES) --> `Mercedes`
        name3 = CarEnum(2000, silent=True) --> None
        name4 = CarEnum(2000) --> raises AttributeError
        name5 = CarEnum(2) --> `BMW`

        :param EnumMember | object value: value to get its name.

        :param bool silent: specifies that if value does not exist in
                            enumeration, does not raise an error and
                            return None instead. defaults to False.

        :raises AttributeError: attribute error.

        :rtype: str
        """

        if silent is True:
            return cls.try_str(value)

        return cls.str(value)

    @classmethod
    def contains(cls, value):
        """
        gets a value indicating that given input exists in the enumeration values.

        :param EnumMember | object value: value to be checked for existence.

        :rtype: bool
        """

        value = cls.get_pure_value(value)
        return value in cls.values()

    @classmethod
    def try_str(cls, value):
        """
        gets the name of given value in enumeration.

        note that if the value is not an `EnumMember` instance, it does not have
        a name and the name of it's attribute will be returned instead.
        if the value does not exist in enumeration, it returns None.

        :param EnumMember | object value: value to get its name.

        :rtype: str
        """

        try:
            return cls.str(value)
        except AttributeError:
            return None


class HTTPMethodEnum(CoreEnum):
    """
    http method enum.
    """

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    TRACE = 'TRACE'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'
    COPY = 'COPY'
    LINK = 'LINK'
    UNLINK = 'UNLINK'
    PURGE = 'PURGE'
    VIEW = 'VIEW'


class InformationResponseCodeEnum(CoreEnum):
    """
    http information response code enum.
    """

    # this interim response indicates that everything so far is OK and that
    # the client should continue with the request or ignore it if it is already finished.
    CONTINUE = 100

    # this code is sent in response to an upgrade request header by the client,
    # and indicates the protocol the server is switching to.
    SWITCHING_PROTOCOL = 101

    # this code indicates that the server has received and
    # is processing the request, but no response is available yet.
    PROCESSING = 102

    # this status code is primarily intended to be used with the Link header to allow
    # the user agent to start preloading resources while the server is still preparing a response.
    EARLY_HINTS = 103


class SuccessfulResponseCodeEnum(CoreEnum):
    """
    http successful response code enum.
    """

    # the request has succeeded. the meaning of a success varies depending on the http method:
    # GET: the resource has been fetched and is transmitted in the message body.
    # HEAD: the entity headers are in the message body.
    # PUT/POST: the resource describing the result of the action is transmitted in the message
    # body.
    # TRACE: the message body contains the request message as received by the server.
    OK = 200

    # the request has succeeded and a new resource has been created as a result of it.
    # this is typically the response sent after a POST request, or after some PUT requests.
    CREATED = 201

    # the request has been received but not yet acted upon. it is non-committal,
    # meaning that there is no way in http to later send an asynchronous response
    # indicating the outcome of processing the request. it is intended for cases where
    # another process or server handles the request, or for batch processing.
    ACCEPTED = 202

    # this response code means returned meta-information set is not exact set as
    # available from the origin server, but collected from a local or a third party copy.
    # except this condition, 200 OK response should be preferred instead of this response.
    NON_AUTHORITATIVE_INFORMATION = 203

    # there is no content to send for this request, but the headers may be useful.
    # the user-agent may update its cached headers for this resource with the new ones.
    NO_CONTENT = 204

    # this response code is sent after accomplishing request
    # to tell user agent reset document view which sent this request.
    RESET_CONTENT = 205

    # this response code is used because of range header sent
    # by the client to separate download into multiple streams.
    PARTIAL_CONTENT = 206

    # a multi-status response conveys information about multiple resources
    # in situations where multiple status codes might be appropriate.
    MULTI_STATUS = 207

    # used inside a DAV: propstat response element to avoid enumerating
    # the internal members of multiple bindings to the same collection repeatedly.
    ALREADY_REPORTED = 208

    # the server has fulfilled a GET request for the resource,
    # and the response is a representation of the result of
    # one or more instance-manipulations applied to the current instance.
    IM_USED = 226


class RedirectionResponseCodeEnum(CoreEnum):
    """
    http redirection response code enum.
    """

    # the request has more than one possible response. the user-agent or user should
    # choose one of them. there is no standardized way of choosing one of the responses.
    MULTIPLE_CHOICE = 300

    # this response code means that the URI of the requested resource
    # has been changed permanently. Probably, the new URI would be given in the response.
    MOVED_PERMANENTLY = 301

    # this response code means that the URI of requested resource has been changed temporarily.
    # new changes in the URI might be made in the future.
    # therefore, this same URI should be used by the client in future requests.
    FOUND = 302

    # the server sent this response to direct the client to get the
    # requested resource at another URI with a GET request.
    SEE_OTHER = 303

    # this is used for caching purposes. it tells the client that the response has not
    # been modified, so the client can continue to use the same cached version of the response.
    NOT_MODIFIED = 304

    # was defined in a previous version of the http specification to indicate that a
    # requested response must be accessed by a proxy. it has been deprecated due to
    # security concerns regarding in-band configuration of a proxy.
    USE_PROXY = 305

    # this response code is no longer used, it is just reserved currently.
    # it was used in a previous version of the http 1.1 specification.
    UNUSED = 306

    # the server sends this response to direct the client to get the requested resource
    # at another URI with same method that was used in the prior request.
    # this has the same semantics as the 302 Found http response code, with the exception
    # that the user agent must not change the http method used: if a POST was used in
    # the first request, a POST must be used in the second request.
    TEMPORARY_REDIRECT = 307

    # this means that the resource is now permanently located at another URI,
    # specified by the Location: http response header. this has the same semantics
    # as the 301 moved permanently http response code, with the exception that
    # the user agent must not change the http method used: if a POST was used in
    # the first request, a POST must be used in the second request.
    PERMANENT_REDIRECT = 308


class ClientErrorResponseCodeEnum(CoreEnum):
    """
    http client error response code enum.
    """

    # this response means that server could not understand the request due to invalid syntax.
    BAD_REQUEST = 400

    # although the http standard specifies "unauthorized", semantically
    # this response means "unauthenticated". that is, the client must authenticate
    # itself to get the requested response.
    UNAUTHORIZED = 401

    # this response code is reserved for future use. initial aim for creating
    # this code was using it for digital payment systems however this is not used currently.
    PAYMENT_REQUIRED = 402

    # The client does not have access rights to the content, i.e. they are unauthorized,
    # so server is rejecting to give proper response. unlike 401, the client's identity
    # is known to the server.
    FORBIDDEN = 403

    # the server can not find requested resource. in the browser, this means the url
    # is not recognized. in an API, this can also mean that the endpoint is valid but the
    # resource itself does not exist. servers may also send this response instead of 403
    # to hide the existence of a resource from an unauthorized client.
    # this response code is probably the most famous one due to its frequent occurrence on the web.
    NOT_FOUND = 404

    # the request method is known by the server but has been disabled and cannot be used.
    # for example, an API may forbid DELETE-ing a resource. The two mandatory methods,
    # GET and HEAD, must never be disabled and should not return this error code.
    METHOD_NOT_ALLOWED = 405

    # this response is sent when the web server, after performing server-driven content
    # negotiation, doesn't find any content following the criteria given by the user agent.
    NOT_ACCEPTABLE = 406

    # this is similar to 401 but authentication is needed to be done by a proxy.
    PROXY_AUTHENTICATION_REQUIRED = 407

    # this response is sent on an idle connection by some servers, even without any previous
    # request by the client. it means that the server would like to shut down this unused
    # connection. this response is used much more since some browsers, like Chrome,
    # Firefox 27+, or IE9, use http pre-connection mechanisms to speed up surfing.
    # also note that some servers merely shut down the connection without sending this message.
    REQUEST_TIMEOUT = 408

    # this response is sent when a request conflicts with the current state of the server.
    CONFLICT = 409

    # this response would be sent when the requested content has been permanently deleted
    # from server, with no forwarding address. clients are expected to remove their caches
    # and links to the resource. The http specification intends this status code to be used
    # for "limited-time, promotional services". APIs should not feel compelled to indicate
    # resources that have been deleted with this status code.
    GONE = 410

    # server rejected the request because the Content-Length header field
    # is not defined and the server requires it.
    LENGTH_REQUIRED = 411

    # the client has indicated preconditions in its headers which the server does not meet.
    PRECONDITION_FAILED = 412

    # request entity is larger than limits defined by server; the server might
    # close the connection or return an Retry-After header field.
    PAYLOAD_TOO_LARGE = 413

    # the URI requested by the client is longer than the server is willing to interpret.
    URI_TOO_LONG = 414

    # the media format of the requested data is not supported by the server,
    # so the server is rejecting the request.
    UNSUPPORTED_MEDIA_TYPE = 415

    # the range specified by the Range header field in the request can't be fulfilled;
    # it's possible that the range is outside the size of the target URI's data.
    REQUESTED_RANGE_NOT_SATISFIABLE = 416

    # this response code means the expectation indicated by the
    # expect request header field can't be met by the server.
    EXPECTATION_FAILED = 417

    # the server refuses the attempt to brew coffee with a teapot.
    IM_A_TEAPOT = 418

    # the request was directed at a server that is not able to produce a response.
    # this can be sent by a server that is not configured to produce responses for
    # the combination of scheme and authority that are included in the request URI.
    MISDIRECTED_REQUEST = 421

    # the request was well-formed but was unable to be followed due to semantic errors.
    UNPROCESSABLE_ENTITY = 422

    # the resource that is being accessed is locked.
    LOCKED = 423

    # the request failed due to failure of a previous request.
    FAILED_DEPENDENCY = 424

    # indicates that the server is unwilling to risk processing a request that might be replayed.
    TOO_EARLY = 425

    # the server refuses to perform the request using the current protocol but might be
    # willing to do so after the client upgrades to a different protocol.
    # the server sends an Upgrade header in a 426 response to indicate the required protocol(s).
    UPGRADE_REQUIRED = 426

    # the origin server requires the request to be conditional. intended to prevent
    # the 'lost update' problem, where a client GETs a resource's state, modifies it,
    # and PUTs it back to the server, when meanwhile a third party has modified the state
    # on the server, leading to a conflict.
    PRECONDITION_REQUIRED = 428

    # the user has sent too many requests in a given amount of time ("rate limiting").
    TOO_MANY_REQUESTS = 429

    # the server is unwilling to process the request because its header fields are too large.
    # the request may be resubmitted after reducing the size of the request header fields.
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431

    # the user requests an illegal resource, such as a web page censored by a government.
    UNAVAILABLE_FOR_LEGAL_REASONS = 451


class ServerErrorResponseCodeEnum(CoreEnum):
    """
    http server error response code enum.
    """

    # the server has encountered a situation it doesn't know how to handle.
    INTERNAL_SERVER_ERROR = 500

    # the request method is not supported by the server and cannot be handled.
    # the only methods that servers are required to support (and therefore that must not
    # return this code) are GET and HEAD.
    NOT_IMPLEMENTED = 501

    # this error response means that the server, while working as a gateway to get
    # a response needed to handle the request, got an invalid response.
    BAD_GATEWAY = 502

    # the server is not ready to handle the request. common causes are a server that
    # is down for maintenance or that is overloaded. Note that together with this response,
    # a user-friendly page explaining the problem should be sent. This responses should be
    # used for temporary conditions and the Retry-After: http header should, if possible,
    # contain the estimated time before the recovery of the service. the webmaster
    # must also take care about the caching-related headers that are sent along with
    # this response, as these temporary condition responses should usually not be cached.
    SERVICE_UNAVAILABLE = 503

    # this error response is given when the server is acting
    # as a gateway and cannot get a response in time.
    GATEWAY_TIMEOUT = 504

    # the http version used in the request is not supported by the server.
    HTTP_VERSION_NOT_SUPPORTED = 505

    # the server has an internal configuration error: transparent content negotiation
    # for the request results in a circular reference.
    VARIANT_ALSO_NEGOTIATES = 506

    # the server has an internal configuration error: the chosen variant resource
    # is configured to engage in transparent content negotiation itself,
    # and is therefore not a proper end point in the negotiation process.
    INSUFFICIENT_STORAGE = 507

    # the server detected an infinite loop while processing the request.
    LOOP_DETECTED = 508

    # further extensions to the request are required for the server to fulfill it.
    NOT_EXTENDED = 510

    # the 511 status code indicates that the client needs to authenticate to gain network access.
    NETWORK_AUTHENTICATION_REQUIRED = 511
