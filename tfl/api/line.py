# -*- coding: utf-8 -*-
from tfl.api import Api
from tfl.lib.validation import validate_input


class Line(Api):

    def valid_modes(self):
        url = self.base_url + "Line/Meta/Modes/"
        response = self._request(url, http_method="GET")
        data = self._check_response(response.json())

        return data

    def severity_codes(self):
        url = self.base_url + "Line/Meta/Severity/"
        response = self._request(url, http_method="GET")
        data = self._check_response(response.json())

        return data

    def disruption_categories(self):
        url = self.base_url + "Line/Meta/DisruptionCategories/"
        response = self._request(url, http_method="GET")
        data = self._check_response(response.json())

        return data

    def service_types(self):
        url = self.base_url + "Line/Meta/ServiceTypes/"
        response = self._request(url, http_method="GET")
        data = self._check_response(response.json())

        return data

    def lines_by_id(self, ids):
        url = self.base_url + "Line/{0}/"
        response = self._request(
            url.format(",".join(validate_input(ids, str, "ids"))),
            http_method="GET"
        )
        data = self._check_response(response.json())

        return data

    def lines_by_mode(self, modes):
        url = self.base_url + "Line/Mode/{0}/"
        response = self._request(
            url.format(validate_input(modes, str, "modes")),
            http_method="GET"
        )
        data = self._check_response(response.json())

        return data

    def line_by_service_type(self, service_type):
        url = self.base_url + "Line/Route/"
        extra_params = {}
        if service_type in self.service_types():
            extra_params["serviceTypes"] = service_type
        response = self._request(
            url, extra_params=extra_params, http_method="GET"
        )
        data = self._check_response(response.json())

        return data

    def line_by_id_service_type(self, ids, service_type):
        url = self.base_url + "Line/%s/Route/"
        extra_params = {}
        if service_type in self.service_types():
            extra_params["serviceTypes"] = service_type
        response = self._request(
            url.format(validate_input(ids, str, "ids")),
            extra_params=extra_params, http_method="GET"
        )
        data = self._check_response(response.json())

        return data

    def line_by_mode_service_type(self, modes, service_type):
        url = self.base_url + "Line/Mode/{0}/Route/"
        extra_params = {}
        if service_type in self.service_types():
            extra_params["serviceTypes"] = service_type
        response = self._request(
            url.format(validate_input(modes, str, "modes")),
            extra_params=extra_params, http_method="GET"
        )
        data = self._check_response(response.json())

        return data
