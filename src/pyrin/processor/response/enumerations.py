# -*- coding: utf-8 -*-
"""
response enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class ResponseHeaderEnum(CoreEnum):
    """
    response header enum.
    """

    # Accept-Patch: text/example;charset=utf-8
    # specifies which patch document formats this server supports.
    ACCEPT_PATCH = 'Accept-Patch'

    # Accept-Ranges: bytes
    # what partial content range types this server supports via byte serving.
    ACCEPT_RANGES = 'Accept-Ranges'

    # Age: 12
    # the age the object has been in a proxy cache in seconds.
    AGE = 'Age'

    # Allow: GET, HEAD
    # valid methods for a specified resource. to be used for a 405 Method not allowed.
    ALLOW = 'Allow'

    # Alt-Svc: http/1.1= "http2.example.com:8001"; ma=7200
    # a server uses “Alt-Svc” header (meaning alternative services) to indicate that its
    # resources can also be accessed at a different network location (host or port) or using
    # a different protocol. when using HTTP/2, servers should instead send an ALTSVC frame.
    ALT_SVC = 'Alt-Svc'

    # Cache-Control: max-age=3600 Cache-Control: no-cache, no-store, max-age=0, must-revalidate
    # if no-cache is used, the 'Cache-Control' header can tell the browser to never use a cached
    # version of a resource without first checking the ETag value.
    # 'max-age' is measured in seconds. the more restrictive 'no-store' option tells the browser
    # (and all the intermediary network devices) not even store the resource in its cache.
    CACHE_CONTROL = 'Cache-Control'

    # Connection: close
    # Control options for the current connection and list of hop-by-hop response fields.
    # deprecated in HTTP/2
    CONNECTION = 'Connection'

    # Content-Disposition: attachment; filename="file.txt"
    # an opportunity to raise a 'File Download' dialogue box for a known MIME type with
    # binary format or suggest a filename for dynamic content. quotes are necessary with
    # special characters.
    CONTENT_DISPOSITION = 'Content-Disposition'

    # Content-Encoding: gzip
    # the type of encoding used on the data.
    CONTENT_ENCODING = 'Content-Encoding'

    # Content-Language: en
    # the natural language or languages of the intended audience for the enclosed content.
    CONTENT_LANGUAGE = 'Content-Language'

    # Content-Length: 348
    # the length of the response body expressed in 8-bit bytes.
    CONTENT_LENGTH = 'Content-Length'

    # Content-Location: /index.htm
    # an alternate location for the returned data.
    CONTENT_LOCATION = 'Content-Location'

    # Content-Range: bytes 21010-47021/47022
    # where in a full body message this partial message belongs.
    CONTENT_RANGE = 'Content-Range'

    # Content-Type: text/html; charset=utf-8
    # the mime type of this content.
    CONTENT_TYPE = 'Content-Type'

    # Date: Tue, 15 Nov 1994 08:12:31 GMT
    # the date and time that the message was sent.
    # (in 'HTTP-date' format as defined by RFC 7231).
    DATE = 'Date'

    # Delta-Base: "abc"
    # specifies the delta-encoding entity tag of the response.
    DELTA_BASE = 'Delta-Base'

    # ETag: "737060cd8c284d8a[...]"
    # an identifier for a specific version of a resource, often a message digest.
    ETAG = 'ETag'

    # Expires: Sat, 01 Dec 2018 16:00:00 GMT
    # gives the date/time after which the response is considered stale.
    # (in 'HTTP-date' format as defined by RFC 7231).
    EXPIRES = 'Expires'

    # IM: feed
    # instance-manipulations applied to the response.
    IM = 'IM'

    # Last-Modified: Mon, 15 Nov 2017 12:00:00 GMT
    # the last modified date for the requested object.
    # (in 'HTTP-date' format as defined by RFC 7231).
    LAST_MODIFIED = 'Last-Modified'

    # Link: </feed>; rel="alternate"
    # used to express a typed relationship with another resource, where the relation
    # type is defined by RFC 5988.
    LINK = 'Link'

    # Location: /pub/WWW/People.html
    # used in redirection, or when a new resource has been created.
    LOCATION = 'Location'

    # Pragma: no-cache
    # implementation-specific fields that may have various effects anywhere along
    # the request-response chain.
    PRAGMA = 'Pragma'

    # Proxy-Authenticate: Basic
    # request authentication to access the proxy.
    PROXY_AUTHENTICATE = 'Proxy-Authenticate'

    # HTTP public key pinning, announces hash of website’s authentic TLS certificate.
    PUBLIC_KEY_PINS = 'Public-Key-Pins'

    # Retry-After: 120 Retry-After: Fri, 07 Nov 2014 23:59:59 GMT
    # if an entity is temporarily unavailable, this instructs the client to try again later.
    # value could be a specified period of time (in seconds) or an 'HTTP-date'.
    RETRY_AFTER = 'Retry-After'

    # Server: Apache/2.4.1 (Unix)
    # a name for the server.
    SERVER = 'Server'

    # Set-Cookie: UserID=JohnDoe; Max-Age=3600; Version=1
    # an HTTP cookie.
    SET_COOKIE = 'Set-Cookie'

    # Strict-Transport-Security: max-age=16070400; includeSubDomains
    # an HSTS policy informing the HTTP client how long to cache the HTTPS only policy
    # and whether this applies to subdomains.
    STRICT_TRANSPORT_SECURITY = 'Strict-Transport-Security'

    # Trailer: Max-Forwards
    # the trailer general field value indicates that the given set of header fields is
    # present in the trailer of a message encoded with chunked transfer coding.
    TRAILER = 'Trailer'

    # Transfer-Encoding: chunked
    # the form of encoding used to safely transfer the entity to the user.
    # currently defined methods are: chunked, compress, deflate, gzip, identity.
    # deprecated in HTTP/2.
    TRANSFER_ENCODING = 'Transfer-Encoding'

    # Tk: ?
    # tracking status header, value suggested to be sent in response to a DNT(do-not-track),
    # possible values: '!' — under construction. '?' — dynamic. 'G' — gateway to multiple parties.
    # 'N' — not tracking. 'T' — tracking. 'C' — tracking with consent. 'P' — tracking only if
    # consented. 'D' — disregarding DNT. 'U' — updated.
    TK = 'Tk'

    # Upgrade: h2c, HTTPS/1.3, IRC/6.9, RTA/x11, websocket
    # ask the client to upgrade to another protocol.
    # deprecated in HTTP/2.
    UPGRADE = 'Upgrade'

    # Vary: Accept-Language Vary: *
    # tells downstream proxies how to match future request headers to decide whether the
    # cached response can be used rather than requesting a fresh one from the origin server.
    VARY = 'Vary'

    # Via: 1.0 fred, 1.1 example.com (Apache/1.1)
    # informs the client of proxies through which the response was sent.
    VIA = 'Via'

    # Warning: 199 Miscellaneous warning
    # a general warning about possible problems with the entity body.
    WARNING = 'Warning'

    # WWW-Authenticate: Basic
    # indicates the authentication scheme that should be used to access the requested entity.
    WWW_AUTHENTICATE = 'WWW-Authenticate'


class NonStandardResponseHeaderEnum(CoreEnum):
    """
    non standard response header enum.
    """

    # helps to protect against XSS attacks.
    CONTENT_SECURITY_POLICY = 'Content-Security-Policy'

    # Refresh: 10;http://www.example.org/
    # redirect to a URL after an arbitrary delay expressed in seconds.
    REFRESH = 'Refresh'

    # X-Powered-By: Brain/0.6b
    # can be used by servers to send their name and version.
    X_POWERED_BY = 'X-Powered-By'

    # allows the server to pass a request id that clients can send
    # back to let the server correlate the request.
    X_REQUEST_ID = 'X-Request-ID'

    # sets which version of Internet Explorer compatibility layer should be used.
    # only used if you need to support IE8 or IE9.
    X_UA_COMPATIBLE = 'X-UA-Compatible'

    # now replaced by the 'Content-Security-Policy' header, used in older browsers
    # to stop pages load when an XSS attack is detected.
    X_XSS_PROTECTION = 'X-XSS-Protection'
