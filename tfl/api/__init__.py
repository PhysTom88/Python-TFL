# -*- coding: utf-8 -*-
import requests
try:
    from urllib.parse import urlparse, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, urlunparse
    from urllib import urlencode

from tfl.api.exceptions import TflError, HttpMethodNotAllowed, HttpResponseError


__all__ = ["Api"]


class Api:
    """
    A python interface into the TfL API
    """
    ALLOWED_METHODS = ["GET"]

    def __init__(self, app_id=None, app_key=None, timeout=None):
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://api.tfl.gov.uk/"
        self.timeout = timeout

        self.validate_credentials(app_id=app_id, app_key=app_key)

    def validate_credentials(self, app_id, app_key):
        if not all([app_id, app_key]):
            raise TflError("Missing App ID or App Key Credentials")

    def _check_response(self, content):
        if isinstance(content, (dict, list)) and 'exceptionType' in content:
            message = "{0}: {1}".format(content['httpStatusCode'],
                                        content['message'])
            raise HttpResponseError(message)
        return content

    def _build_absolute_url(self, url, get_params=None):
        (scheme, netloc, path, params, query, fragment) = urlparse(url)
        if get_params and len(get_params) > 0:
            if not isinstance(get_params, dict):
                raise TflError("\"get_params\" must be a dict.")

            extra_parameters = urlencode(
                dict((k, v) for k, v in get_params.items()
                     if v is not None))
            if query:
                query += '&' + extra_parameters
            else:
                query = extra_parameters

            return urlunparse((scheme, netloc, path, params, query, fragment))

    def _request(self, url, http_method, extra_params=None, authenticate=True):
        if authenticate and not (self.app_id and self.app_key):
            raise TflError(
                "The Tfl.Api instance requires authentication to function")
        get_params = {"app_id": self.app_id, "app_key": self.app_key}
        if extra_params:
            get_params.update(extra_params)

        if http_method not in self.ALLOWED_METHODS:
            raise HttpMethodNotAllowed("{0}".format(http_method))
        else:
            url = self._build_absolute_url(url, get_params=get_params)
            response = requests.get(url, timeout=self.timeout)

        return response