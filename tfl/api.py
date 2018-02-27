
# -*- coding: utf-8 -*-
import requests
try:
    from urllib.parse import urlparse, urlunparse, urlencode
except ImportError:
    from urlparse import urlparse, urlunparse
    from urllib import urlencode

from tfl import (
    Accident,
    AirQuality,
    BikePoint,
    Cabwise,
    JourneyMode
)

from tfl.exceptions import TflError
from tfl.utils import validate_year, validate_number, validate_boolean


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
            raise TflError("Missing App ID or App Key Credentials")
        self.app_id = app_id
        self.app_key = app_key

    def GetAccidentStats(self, year):
        url = self.base_url + "AccidentStats/{0}/"
        year = validate_year(str(year))
        response = self._Request(url.format(year), http_method="GET")
        data = self._CheckResponse(response.json())

        return [Accident.fromJson(x) for x in data]

    def GetAirQuality(self):
        url = self.base_url + "AirQuality/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json().get('currentForecast'))

        return [AirQuality.fromJSON(x) for x in data]

    def GetBikePoints(self):
        url = self.base_url + "BikePoint/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json())

        return [BikePoint.fromJSON(b) for b in data]

    def GetBikePoint(self, point):
        url = self.base_url + "BikePoint/{0}"
        response = self._Request(url.format(point), http_method="GET")
        data = self._CheckResponse(response.json())

        return BikePoint.fromJSON(data)

    def GetJourneyModes(self):
        url = self.base_url + "Journey/Meta/Modes/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json())

        return [JourneyMode.fromJSON(j) for j in data]

    def SearchBikePoints(self, query):
        url = self.base_url + "BikePoint/Search/"
        extra_params = {"query": query}
        response = self._Request(
            url, extra_params=extra_params, http_method="GET")
        data = self._CheckResponse(response.json())

        return [BikePoint.fromJSON(b) for b in data]

    def SearchCabwise(
            self, lat, lon, optype=None, wc=None, radius=None,
            name=None, maxResults=None, legacy_format=True,
            twentyfour_seven=True):
        url = self.base_url + "Cabwise/Search"
        extra_params = {}
        extra_params["lat"] = validate_number(lat)
        extra_params["lon"] = validate_number(lon)

        if radius:
            extra_params["radius"] = validate_number(radius)
        if maxResults:
            extra_params["maxResults"] = validate_number(maxResults)
        if twentyfour_seven is not None:
            extra_params["twentyfour_seven"] = validate_boolean(
                twentyfour_seven)
        response = self._Request(
            url, extra_params=extra_params, http_method="GET")
        data = self._CheckResponse(
            response.json()["Operators"]["OperatorList"])

        return [Cabwise.fromJSON(c) for c in data]

    def _CheckResponse(self, content):
        if isinstance(content, (dict, list)) and 'exceptionType' in content:
            message = "{0}: {1}".format(content['httpStatusCode'],
                                        content['message'])
            raise TflError(message)
        return content

    def _BuildAbsoluteURL(self, url, get_params=None):
        (scheme, netloc, path, params, query, fragment) = urlparse(url)
        if get_params and len(get_params) > 0:
            if not isinstance(get_params, dict):
                raise TflError("\"get_params\" must be a dict.")

            extra_parameters = urlencode(
                dict((_k, _v) for _k, _v in get_params.items()
                     if _v is not None))
            if query:
                query += '&' + extra_parameters
            else:
                query = extra_parameters

            return urlunparse((scheme, netloc, path, params, query, fragment))

    def _Request(self, url, http_method, extra_params=None, authenticate=True):
        if authenticate and not (self.app_id and self.app_key):
            raise TflError(
                "The Tfl.Api instance requires authentication to function")
        get_params = {"app_id": self.app_id, "app_key": self.app_key}
        if extra_params:
            get_params.update(extra_params)

        if http_method != "GET":
            raise NotImplementedError
        else:
            url = self._BuildAbsoluteURL(url, get_params=get_params)
            response = requests.get(url, timeout=self._timeout)

        return response
