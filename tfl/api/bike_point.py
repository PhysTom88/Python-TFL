# -*- coding: utf-8 -*-
from tfl.api import Api


class BikePoint(Api):

    def all_points(self):
        url = self.base_url + "BikePoint/"
        response = self._request(url, http_method="GET")
        data = self._check_response(response.json())

        return data

    def bike_point_data(self, point):
        url = self.base_url + "BikePoint/{0}"
        response = self._request(url.format(point), http_method="GET")
        data = self._check_response(response.json())

        return data

    def search(self, query):
        url = self.base_url + "BikePoint/Search/"
        extra_params = {"query": query}
        response = self._request(
            url, extra_params=extra_params, http_method="GET")
        data = self._check_response(response.json())

        return data