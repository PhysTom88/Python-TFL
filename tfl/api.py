
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
    Point,
    Cabwise,
    JourneyMode,
    JourneyDisambiguation,
    JourneyPlanner,
    Line,
    LineStatusSeverity
)

from tfl.exceptions import TflError
from tfl.utils import validate_year, validate_input


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

        return [Accident.fromJSON(x) for x in data]

    def GetAirQuality(self):
        url = self.base_url + "AirQuality/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json().get('currentForecast'))

        return [AirQuality.fromJSON(x) for x in data]

    def GetBikePoints(self):
        url = self.base_url + "BikePoint/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json())

        return [Point.fromJSON(b) for b in data]

    def GetBikePoint(self, point):
        url = self.base_url + "BikePoint/{0}"
        response = self._Request(url.format(point), http_method="GET")
        data = self._CheckResponse(response.json())

        return Point.fromJSON(data)

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

        return [Point.fromJSON(b) for b in data]

    def SearchCabwise(
            self, lat, lon, optype=None, wc=None, radius=None,
            name=None, maxResults=None, legacy_format=True,
            twentyfour_seven=True):
        url = self.base_url + "Cabwise/Search"
        extra_params = {}
        extra_params["lat"] = validate_input(lat, float, "lat")
        extra_params["lon"] = validate_input(lon, float, "lon")

        if radius:
            extra_params["radius"] = validate_input(radius, float, "radius")
        if maxResults:
            extra_params["maxResults"] = validate_input(
                maxResults, int, "maxResults"
            )
        if twentyfour_seven is not None:
            extra_params["twentyfour_seven"] = validate_input(
                twentyfour_seven, bool, "twentyfour_seven"
            )
        response = self._Request(
            url, extra_params=extra_params, http_method="GET")
        data = self._CheckResponse(
            response.json()["Operators"]["OperatorList"])

        return [Cabwise.fromJSON(c) for c in data]

    def SearchJourneyPlanner(
            self, _from, to, via=None, nationalSearch=False, date=None,
            time=None, timels=None, journeyPreference=None, mode=None,
            accessibilityPreference=None, fromName=None, toName=None,
            viaName=None, maxTransferMinutes=None, maxWalkingMinutes=None,
            walkingSpeed=None, cyclePreference=None, adjustment=None,
            bikeProficiency=None, alternativeCycle=None,
            alternativeWalking=None, useMultiModalCall=None,
            walkingOptimsation=False, taxiOnlyTrip=False):
        url = self.base_url + "Journey/JourneyResults/{0}/to/{1}"

        extra_params = {}
        if via is not None:
            extra_params["via"] = validate_input(via, str, "via")
        if nationalSearch is not None:
            extra_params["nationalSearch"] = validate_input(
                nationalSearch, bool, "nationalSearch"
            )
        if date is not None:
            extra_params["date"] = validate_input(date, str, "data")
        if time is not None:
            extra_params["time"] = validate_input(time, str, "time")
        if timels in ["Arriving", "Departing"]:
            extra_params["timels"] = timels
        if journeyPreference in ["LeastInterchange", "LeastWalking",
                                 "leastTime"]:
            extra_params["journeyPreference"] = journeyPreference
        if mode is not None:
            if isinstance(mode, (tuple, list)):
                extra_params["mode"] = ','.join(
                    [validate_input(m) for m in mode])
            else:
                extra_params["mode"] = validate_input(mode, str, "mode")
        if (accessibilityPreference in
            ["noSolidStairs", "noEscalators", "noElavators",
             "stepFreeToVehicle", "stepFreeToPlatform"]):
            extra_params["accessibilityPreference"] = accessibilityPreference
        if fromName is not None:
            extra_params["fromName"] = validate_input(
                fromName, str, "fromName")
        if toName is not None:
            extra_params["toName"] = validate_input(toName, str, "toName")
        if viaName is not None:
            extra_params["viaName"] = validate_input(viaName, str, "viaName")
        if maxTransferMinutes is not None:
            extra_params["maxTransferMinutes"] = str(validate_input(
                maxTransferMinutes, int, "maxTransferMinutes")
            )
        if maxWalkingMinutes is not None:
            extra_params["maxWalkingMinutes"] = str(
                validate_input(maxWalkingMinutes, int, "maxWalkingMinutes")
            )
        if walkingSpeed in ["Slow", "Average", "Fast"]:
            extra_params["walkingSpeed"] = walkingSpeed
        if (cyclePreference in
                ["AllTheWay", "LeaveAtStation", "TakeOnTransport",
                 "CycleHire"]):
            extra_params["cyclePreference"] = cyclePreference
        if adjustment in ["TripFirst", "TripLast"]:
            extra_params["adjustment"] = adjustment
        if bikeProficiency in ["Easy", "Moderate", "Fast"]:
            extra_params["bikeProficiency"] = bikeProficiency
        if alternativeCycle is not None:
            extra_params["alternativeCycle"] = validate_input(
                alternativeCycle, bool, "alternativeCycle")
        if useMultiModalCall is not None:
            extra_params["useMultiModalCall"] = validate_input(
                useMultiModalCall, bool, "useMultiModalCall")
        if walkingOptimsation is not None:
            extra_params["walkingOptimsation"] = validate_input(
                walkingOptimsation, bool, "walkingOptimsation")
        if taxiOnlyTrip is not None:
            extra_params["taxiOnlyTrip"] = validate_input(
                taxiOnlyTrip, bool, "taxiOnlyTrip")

        response = self._Request(
            url.format(
                validate_input(_from, str, "_from"),
                validate_input(to, str, "to")),
            extra_params=extra_params, http_method="GET")
        data = self._CheckResponse(
            response.json()
        )

        if "DisambiguationResult" in data["$type"]:
            return JourneyDisambiguation.fromJSON(data)
        else:
            return JourneyPlanner.fromJSON(data)

    def GetLineModes(self):
        url = self.base_url + "Line/Meta/Modes/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json())

        return [JourneyMode.fromJSON(j) for j in data]

    def GetLineSeverityCodes(self):
        url = self.base_url + "Line/Meta/Severity/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json())

        return [LineStatusSeverity.fromJSON(l) for l in data]

    def GetLineDisruptionCategories(self):
        url = self.base_url + "Line/Meta/DisruptionCategories/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json())

        return [category for category in data]

    def GetLineServiceTypes(self):
        url = self.base_url + "Line/Meta/ServiceTypes/"
        response = self._Request(url, http_method="GET")
        data = self._CheckResponse(response.json())

        return [service for service in data]

    def GetLines(self, ids):
        url = self.base_url + "Line/{0}/"
        response = self._Request(
            url.format(",".join(validate_input(ids, list, "ids"))),
            http_method="GET"
        )
        data = self._CheckResponse(
            response.json()
        )

        return [Line.fromJSON(l) for l in data]

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
