# -*- coding: utf-8 -*-
from tfl.api import Api
from tfl.api.exceptions import InvalidInputError
from tfl.lib.validation import validate_input, validate_datestring
from tfl.lib.utils import sensible_string_list


class Line(Api):

    DIRECTIONS = ["inbound", "outbound", "all"]

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

    def line_routes(self, line_id, direction, service_type=None, exclude_crowding=True):
        url = self.base_url + "Line/{0}/Route/Sequence/{1}/"
        if direction not in self.DIRECTIONS:
            raise InvalidInputError("direction value must be:{0}".format(sensible_string_list(self.DIRECTIONS)))

        extra_params = {}
        if service_type in self.service_types():
            extra_params["serviceTypes"] = service_type
        if exclude_crowding is not None:
            extra_params["excludeCrowding"] = validate_input(exclude_crowding, bool, "exclude_crowding")

        response = self._request(
            url.format(
                validate_input(line_id, str, "line_id"),
                direction),
            extra_params=extra_params, http_method="GET")
        data = self._check_response(response.json())

        return data

    def line_status_by_date(self, ids, start_date, end_date, detail=True):
        url = self.base_url + "/Line/{0}/Status/{1}/to/{2}"
        valid_start = validate_datestring(start_date, string_format="%Y-%m-%d")
        valid_end = validate_datestring(end_date, string_format="%Y-%m-%d")

        extra_params = {}
        if detail is not None:
            extra_params["detail"] = validate_input(detail, bool, "detail")

        response = self._request(
            url.format(validate_input(ids, str, "ids"), valid_start, valid_end),
            extra_params=extra_params, http_method="GET")
        data = self._check_response(response.json())

        return data

    def current_line_status(self, ids, detail=True):
        url = self.base_url + "/Line/{0}/Status/"

        extra_params = {}
        if detail is not None:
            extra_params["detail"] = validate_input(detail, bool, "detail")

        response = self._request(
            url.format(validate_input(ids, str, "ids")),
            extra_params=extra_params, http_method="GET")
        data = self._check_response(response.json())

        return data

    def line_search(self, query, modes=None, service_type=None):
        url = self.base_url + "Line/Search/{0}"
        extra_params = {}
        if modes:
            extra_params["modes"] = validate_input(modes, str, "mode")
        if service_type in self.service_types():
            extra_params["serviceTypes"] = service_type

        response = self._request(
            url.format(validate_input(query, str, "query")),
            extra_params=extra_params, http_method="GET")
        data = self._check_response(response.json())

        return data
