# -*- coding: utf-8 -*-
from tfl.api import Api
from tfl.lib.validation import validate_year


class AccidentData(Api):

    def accident_stats_by_year(self, year):
        url = self.base_url + "AccidentStats/{0}/"
        clean_year = validate_year(year)
        response = self._request(url.format(clean_year), http_method="GET")
        data = self._check_response(response.json())

        return data