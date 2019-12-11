# -*- coding: utf-8 -*-
from tfl.api import Api
from tfl.api.line import Line
from tfl.api.exceptions import InvalidInputError
from tfl.lib.validation import validate_input


class Mode(Api):

    def active_service_types(self):
        url = self.base_url + "Mode/ActiveServiceTypes/"

        response = self._request(url, http_method="GET")
        data = self._check_response(response.json())

        return data

    def mode_arrival_predictions(self, mode, count=None):
        url = self.base_url + "Mode/{0}/Arrivals/"
        modes = [m["modeName"] for m in Line(app_id=self.app_id, app_key=self.app_key).valid_modes()]

        if mode in modes:
            extra_params = {}
            if count is not None:
                extra_params["count"] = validate_input(count, int, "count")

            response = self._request(url.format(mode), extra_params=extra_params, http_method="GET")
            data = self._check_response(response.json())

            return data
        else:
            raise InvalidInputError("'{0}' not a valid mode".format(mode))
