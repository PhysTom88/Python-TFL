
# -*- coding: utf-8 -*-
import json
import requests
try:
    from urllib.parse import urlparse, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, urlunparse
    from urllib import urlencode

from tfl import (
    Accident,
    AirQuality
)

from tfl.exceptions import TflError
from tfl.utils import validate_year


class Api(object):
    """
    A python interface into the TFL api
    """
    def __init__(self, app_id=None, app_key=None, timeout=None):
        self.credentials(app_id, app_key)
        self.base_url = "https://api.tfl.gov.uk/"
        self._timeout = timeout

    def credentials(self, app_id, app_key):
        if not all([app_id, app_key]):
            raise TflError({
                "message": "Missing App ID or App Key Credentials"
            })
        self.app_id = app_id
        self.app_key = app_key

    def GetAccidentStats(self, year):
        url = self.base_url + "AccidentStats/{0}/"
        if not validate_year(year):
            raise TflError({
                "message": "\"Year\" is in incorrect format"
            })
        response = self._Request(url.format(year), http_method="GET")
        data = self._CheckResponse(response.content.decode("utf-8"))

        return [Accident.fromJson(x) for x in data]

    def GetAirQuality(self):
        url = self.base_url + "AirQuality/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json().get('currentForecast'))

        return [AirQuality.fromJSON() for x in data]

    def _CheckResponse(self, content):
        try:
            data = json.loads(content)
        except ValueError:
            raise TflError({
                "message": "Error Recieved: {0}".format(content)
            })

        if 'exceptionType' in data:
            message = "{0}: {1}".format(data['httpStatusCode'],
                                        data['message'])
            raise TflError({"message": message})
        return data

    def _BuildAbsoluteURL(self, url, get_params=None):
        (scheme, netloc, path, params, query, fragment) = urlparse(url)
        if get_params and len(get_params) > 0:
            if not isinstance(get_params, dict):
                raise TflError({
                    "message": "\"get_params\" must be a dict."
                })
            extra_parameters = urlencode(
                dict(_k, _v) for _k, _v in get_params.items()
                if _v is not None)
            if query:
                query += '&' + extra_parameters
            else:
                query = extra_parameters

            return urlunparse((scheme, netloc, path, params, query, fragment))

    def _Request(self, url, http_method, extra_params=None, authenticate=True):
        if authenticate and not (self.app_id and self.app_key):
            raise TflError({
                "message": """The Tfl.Api instance requires "
                              authentication to function"""
            })
        get_params = {"app_id": self.app_id, "app_key": self.app_key}
        if extra_params:
            get_params.update(extra_params)

        if http_method != "GET":
            raise NotImplementedError
        else:
            url = self._BuildAbsoluteURL(url, get_params=get_params)
            response = requests.get(url, timeout=self._timeout)

        return response
