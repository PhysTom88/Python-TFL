# -*- coding: utf-8 -*-
from tfl.api import Api


class AirQuality(Api):

    def air_quality(self):
        url = self.base_url + "AirQuality/"
        response = self._request(url, http_method="GET")
        data = self._check_response(response.json().get('currentForecast'))

        return data