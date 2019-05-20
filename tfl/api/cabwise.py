# -*- coding: utf-8 -*-
from tfl.api import Api
from tfl.lib.utils import stringify_boolean
from tfl.lib.validation import validate_input, validate_latitude, validate_longitude


class Cabwise(Api):

    ALLOWED_OPTYPES = [""]

    def search(
            self, lat, lon, optype=None, wc=None, radius=None,
            name=None, max_results=None, legacy_format=False,
            twentyfour_seven=True):

        url = self.base_url + "Cabwise/Search"
        extra_params = dict()
        extra_params["lat"] = validate_latitude(lat)
        extra_params["lon"] = validate_longitude(lon)
        if optype and optype in self.ALLOWED_OPTYPES:
            extra_params["optype"] = optype
        if wc:
            extra_params["wc"] = stringify_boolean(wc)
        if radius:
            extra_params["radius"] = validate_input(radius, float, "radius")
        if name:
            extra_params["name"] = name
        if max_results:
            extra_params["maxResults"] = validate_input(
                max_results, int, "maxResults"
            )
        if legacy_format is not None:
            extra_params["legacy_format"] = validate_input(legacy_format, bool, "legacy_format")
        if twentyfour_seven is not None:
            extra_params["twentyfour_seven"] = validate_input(
                twentyfour_seven, bool, "twentyfour_seven"
            )
        response = self._request(
            url, extra_params=extra_params, http_method="GET")
        data = self._check_response(
            response.json())

        return data