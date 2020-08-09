# -*- coding: utf-8 -*-
"""
request enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class RequestHeaderEnum(CoreEnum):
    """
    request header enum.
    """

    # A-IM: feed
    # instance manipulations that are acceptable in the response.
    A_IM = 'A-IM'

    # Accept: application/json
    # the media type/types acceptable.
    ACCEPT = 'Accept'

    # Accept-Charset: utf-8
    # the charset acceptable.
    ACCEPT_CHARSET = 'Accept-Charset'

    # Accept-Encoding: gzip, deflate
    # list of acceptable encodings.
    ACCEPT_ENCODING = 'Accept-Encoding'

    # Accept-Language: en-US
    # list of acceptable languages.
    ACCEPT_LANGUAGE = 'Accept-Language'

    # Accept-Datetime: Thu, 31 May 2007 20:35:00 GMT
    # request a past version of the resource prior to the datetime passed.
    ACCEPT_DATETIME = 'Accept-Datetime'

    # Access-Control-Request-Method: GET
    # used in a CORS request.
    ACCESS_CONTROL_REQUEST_METHOD = 'Access-Control-Request-Method'

    # Access-Control-Request-Headers: origin, x-requested-with, accept
    # used in a CORS request.
    ACCESS_CONTROL_REQUEST_HEADERS = 'Access-Control-Request-Headers'

    # Authorization: Basic 34i3j4iom2323==
    # HTTP basic authentication credentials.
    AUTHORIZATION = 'Authorization'

    # Cache-Control: no-cache
    # set the caching rules.
    CACHE_CONTROL = 'Cache-Control'

    # Connection: keep-alive
    # control options for the current connection.
    # Accepts 'keep-alive' and 'close'.
    # deprecated in HTTP/2.
    CONNECTION = 'Connection'

    # Content-Length: 348
    # the length of the request body in bytes.
    CONTENT_LENGTH = 'Content-Length'

    # Content-Type: application/x-www-form-urlencoded
    # the content type of the body of the request (used in POST and PUT requests).
    CONTENT_TYPE = 'Content-Type'

    # Cookie: name=value; Secure; HttpOnly
    COOKIE = 'Cookie'

    # Date: Tue, 15 Nov 1994 08:12:31 GMT
    # the date and time that the request was sent.
    DATE = 'Date'

    # Expect: 100-continue
    # it’s typically used when sending a large request body. we expect the server to
    # return back a '100 Continue' HTTP status if it can handle the request, or
    # '417 Expectation Failed' if not.
    EXPECT = 'Expect'

    # Forwarded: for=192.0.2.60; proto=http; by=203.0.113.43
    # disclose original information of a client connecting to a web server through an
    # HTTP proxy. used for testing purposes only, as it discloses privacy sensitive information.
    FORWARDED = 'Forwarded'

    # From: user@example.com
    # the email address of the user making the request. meant to be used, for example,
    # to indicate a contact email for bots.
    FROM = 'From'

    # Host: flaviocopes.com
    # the domain name of the server (used to determined the server with virtual hosting), and
    # the TCP port number on which the server is listening. if the port is omitted, 80 is
    # assumed. this is a mandatory HTTP request header.
    HOST = 'Host'

    # If-Match: "737060cd8c284d8582d"
    # given one (or more) ETags, the server should only send back the response if the
    # current resource matches one of those ETags. mainly used in PUT methods to update
    # a resource only if it has not been modified since the user last updated it.
    IF_MATCH = 'If-Match'

    # If-Modified-Since: Sat, 29 Oct 1994 19:43:31 GMT
    # allows to return a '304 Not Modified' response header if the content is unchanged
    # since that date.
    IF_MODIFIED_SINCE = 'If-Modified-Since'

    # If-None-Match: "737060cd882f209582d"
    # allows a '304 Not Modified' response header to be returned if content is unchanged.
    # opposite of If-Match.
    IF_NONE_MATCH = 'If-None-Match'

    # If-Range: "737060cd8c9582d"
    # used to resume downloads, returns a partial if the condition is matched (ETag or date)
    # or the full resource if not.
    IF_RANGE = 'If-Range'

    # If-Unmodified-Since: Sat, 29 Oct 1994 19:43:31 GMT
    # only send the response if the entity has not been modified since the specified time.
    IF_UNMODIFIED_SINCE = 'If-Unmodified-Since'

    # Max-Forwards: 10
    # limit the number of times the message can be forwarded through proxies or gateways.
    MAX_FORWARDS = 'Max-Forwards'

    # Origin: http://mydomain.com
    # send the current domain to perform a CORS request, used in an OPTIONS HTTP request.
    # (to ask the server for Access-Control- response headers).
    ORIGIN = 'Origin'

    # Pragma: no-cache
    # used for backwards compatibility with HTTP/1.0 caches.
    PRAGMA = 'Pragma'

    # Proxy-Authorization: Basic 2323jiojioIJOIOJIJ==
    # authorization credentials for connecting to a proxy.
    PROXY_AUTHORIZATION = 'Proxy-Authorization'

    # Range: bytes=500-999
    # request only a specific part of a resource.
    RANGE = 'Range'

    # Referer: https://flaviocopes.com
    # the address of the previous web page from which a link to the currently requested
    # page was followed.
    REFERER = 'Referer'

    # TE: trailers, deflate
    # specify the encodings the client can accept.
    # accepted values: compress, deflate, gzip, trailers.
    # only trailers is supported in HTTP/2.
    TE = 'TE'

    # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
    # AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
    # the string that identifies the user agent.
    USER_AGENT = 'User-Agent'

    # Upgrade: h2c, HTTPS/1.3, IRC/6.9, RTA/x11, websocket
    # ask the server to upgrade to another protocol.
    # deprecated in HTTP/2.
    UPGRADE = 'Upgrade'

    # Via: 1.0 fred, 1.1 example.com (Apache/1.1)
    # informs the server of proxies through which the request was sent.
    VIA = 'Via'

    # Warning: 199 Miscellaneous warning
    # a general warning about possible problems with the status of the message.
    # see https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Warning
    # for range of values.
    WARNING = 'Warning'


class NonStandardRequestHeaderEnum(CoreEnum):
    """
    non standard request header enum.
    """

    # DNT: 1
    # if enabled, asks servers to not track the user.
    DNT = 'Dnt'

    # X-Requested-With: XMLHttpRequest
    # identifies XHR requests.
    X_REQUESTED_WITH = 'X-Requested-With'

    # X-CSRF-Token: <TOKEN>
    # used to prevent CSRF.
    X_CSRF_TOKEN = 'X-CSRF-Token'
