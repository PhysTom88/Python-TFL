import calendar
import json
import unittest

import tfl


class BikePointTest(unittest.TestCase):

    SAMPLE_JSON = '''{"lon": -0.144083, "url": "/Place/BikePoints_76", "commonName": "Longford Street, The Regent's Park", "placeType": "BikePoint", "lat": 51.525595, "id": "BikePoints_76"}'''

    def _SampleBikePoint(self):
        return tfl.BikePoint(
            id="BikePoints_76",
            url="/Place/BikePoints_76",
            commonName="Longford Street, The Regent's Park",
            placeType="BikePoint",
            lat=51.525595,
            lon=-0.144083
        )

    def test_parameters(self):
        bike_point = tfl.BikePoint()
        bike_point.id = "BikePoints_76"
        self.assertEqual("BikePoints_76", bike_point.id)

        bike_point.url = "/Place/BikePoints_76"
        self.assertEqual("/Place/BikePoints_76", bike_point.url)

        bike_point.commonName = "Longford Street, The Regent's Park"
        self.assertEqual(
            "Longford Street, The Regent's Park", bike_point.commonName)

        bike_point.placeType = "BikePoint"
        self.assertEqual("BikePoint", bike_point.placeType)

        bike_point.lat = 51.525595
        self.assertEqual(51.525595, bike_point.lat)

        bike_point.lon = -0.144083
        self.assertEqual(-0.144083, bike_point.lon)

    def test_to_dict(self):
        bike_point = self._SampleBikePoint()
        data = bike_point.toDict()
        self.assertEqual("BikePoints_76", data["id"])
        self.assertEqual("/Place/BikePoints_76", data["url"])
        self.assertEqual(
            "Longford Street, The Regent's Park", data["commonName"])
        self.assertEqual("BikePoint", data["placeType"])
        self.assertEqual(51.525595, data["lat"])
        self.assertEqual(-0.144083, data["lon"])

    def test_from_json(self):
        data = json.loads(self.SAMPLE_JSON)
        bike_point = tfl.BikePoint.fromJSON(data)
        self.assertEqual(self._SampleBikePoint(), bike_point)
