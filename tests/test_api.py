# encoding: utf-8
from __future__ import unicode_literals

import os
import unittest

import tfl


class TestTflApi(unittest.TestCase):

    def setUp(self):
        self.app_id = os.environ.get("APP_ID")
        self.app_key = os.environ.get("APP_KEY")
        self.base_url = "https://api.tfl.gov.uk/"

    def test_api_credentials(self):
        api = tfl.Api(app_id="test", app_key="test")
        self.assertTrue(all([api.app_id, api.app_key]))
        self.assertEqual(self.base_url, api.base_url)

    def test_api_no_credentials(self):
        self.assertRaises(tfl.TflError, lambda: tfl.Api())

    def test_accident_correct_year(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        accidents = api.GetAccidentStats(2016)
        self.assertTrue(isinstance(accidents, (list, tuple, set)))
        self.assertGreater(len(accidents), 0)

        accident = accidents[0]
        self.assertTrue(isinstance(accident, tfl.Accident))
        self.assertGreater(len(accident.vehicles), 0)
        self.assertTrue(isinstance(
            accident.vehicles[0], tfl.AccidentVehicle))
        self.assertGreater(len(accident.casualties), 0)
        self.assertTrue(isinstance(accident.casualties[0], tfl.Casualty))

    def test_accident_incorrect_year(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        self.assertRaises(tfl.TflError, lambda: api.GetAccidentStats(1901))

    def test_accident_incorrect_format(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        self.assertRaises(
            tfl.TflError, lambda: api.GetAccidentStats("Invalid Year")
        )

    def test_air_quality(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        air_quality = api.GetAirQuality()

        self.assertEqual(len(air_quality), 2)
        self.assertTrue(isinstance(air_quality[0], tfl.AirQuality))

    def test_bike_points(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        bike_points = api.GetBikePoints()
        self.assertTrue(isinstance(bike_points, (list, tuple, set)))
        self.assertGreater(len(bike_points), 0)

        bike_point = bike_points[0]
        self.assertTrue(isinstance(bike_point, tfl.BikePoint))
        self.assertGreater(len(bike_point.additionalProperties), 0)
        self.assertTrue(isinstance(
            bike_point.additionalProperties[0], tfl.BpProperty)
        )

    def test_bike_point_correct(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        bike_point = api.GetBikePoint("BikePoints_76")

        self.assertTrue(isinstance(bike_point, tfl.BikePoint))
        self.assertGreater(len(bike_point.additionalProperties), 0)
        self.assertTrue(isinstance(
            bike_point.additionalProperties[0], tfl.BpProperty)
        )

    def test_bike_point_incorrect(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        self.assertRaises(
            tfl.TflError, lambda: api.GetBikePoint("Invalid_BikePoint")
        )

    def test_bike_point_search_correct(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        bike_points = api.SearchBikePoints("St James")
        self.assertTrue(isinstance(bike_points, (list, tuple, set)))
        self.assertGreater(len(bike_points), 0)

        bike_point = bike_points[0]
        self.assertTrue(isinstance(bike_point, tfl.BikePoint))

    def test_bike_point_search_invalid(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        bike_points = api.SearchBikePoints("Nowhere in London")
        self.assertEqual(len(bike_points), 0)

    def test_journey_mode(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        modes = api.GetJourneyModes()
        self.assertGreater(len(modes), 0)
        self.assertTrue(isinstance(modes[0], tfl.JourneyMode))
