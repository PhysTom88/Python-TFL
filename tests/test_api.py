# encoding: utf-8
from __future__ import unicode_literals

import os
import re
import responses
import unittest

import tfl


DEFAULT_URL = re.compile(r'https?://.*\.tfl.gov.uk/.*')


class TestTflApi(unittest.TestCase):

    def setUp(self):
        self.app_id = os.environ.get("APP_ID")
        self.app_key = os.environ.get("APP_KEY")
        self.api = tfl.Api(app_id=self.app_id, app_key=self.app_key)

    def test_api_credentials(self):
        api = tfl.Api(app_id="test", app_key="test")
        self.assertTrue(all([api.app_id, api.app_key]))

    def test_api_no_credentials(self):
        self.assertRaises(tfl.TflError, lambda: tfl.Api())

    @responses.activate
    def test_accident_correct_year(self):
        with open("tests/testdata/accident_correct.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        accidents = self.api.GetAccidentStats(2016)
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
        with open("tests/testdata/accident_incorrect_year.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        self.assertRaises(
            tfl.TflError, lambda: self.api.GetAccidentStats(1901)
        )

    def test_accident_incorrect_format(self):
        with open("tests/testdata/accident_incorrect_format.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        self.assertRaises(
            tfl.TflError, lambda: self.api.GetAccidentStats("Invalid Year")
        )

    def test_air_quality(self):
        air_quality = self.api.GetAirQuality()

        self.assertEqual(len(air_quality), 2)
        self.assertTrue(isinstance(air_quality[0], tfl.AirQuality))

    def test_bike_points(self):
        bike_points = self.api.GetBikePoints()
        self.assertTrue(isinstance(bike_points, (list, tuple, set)))
        self.assertGreater(len(bike_points), 0)

        bike_point = bike_points[0]
        self.assertTrue(isinstance(bike_point, tfl.Point))
        self.assertGreater(len(bike_point.additionalProperties), 0)
        self.assertTrue(isinstance(
            bike_point.additionalProperties[0], tfl.AdditionalProperty)
        )

    def test_bike_point_correct(self):
        bike_point = self.api.GetBikePoint("BikePoints_76")

        self.assertTrue(isinstance(bike_point, tfl.Point))
        self.assertGreater(len(bike_point.additionalProperties), 0)
        self.assertTrue(isinstance(
            bike_point.additionalProperties[0], tfl.AdditionalProperty)
        )

    def test_bike_point_incorrect(self):
        self.assertRaises(
            tfl.TflError, lambda: self.api.GetBikePoint("Invalid_BikePoint")
        )

    def test_bike_point_search_correct(self):
        bike_points = self.api.SearchBikePoints("St James")
        self.assertTrue(isinstance(bike_points, (list, tuple, set)))
        self.assertGreater(len(bike_points), 0)

        bike_point = bike_points[0]
        self.assertTrue(isinstance(bike_point, tfl.Point))

    def test_bike_point_search_invalid(self):
        bike_points = self.api.SearchBikePoints("Nowhere in London")
        self.assertEqual(len(bike_points), 0)

    def test_cabwise_correct_no_options(self):
        cabwise = self.api.SearchCabwise(lat=51.5033, lon=-0.12763)
        self.assertTrue(isinstance(cabwise, (list, tuple, set)))
        self.assertGreater(len(cabwise), 0)

        cab = cabwise[0]
        self.assertTrue(isinstance(cab, tfl.Cabwise))

    def test_cabwise_correct_extra_params(self):
        cabwise = self.api.SearchCabwise(
            lat=51.5033, lon=-0.12763, optype="Minicab",
            radius=2000, maxResults=1)
        self.assertTrue(isinstance(cabwise, (list, tuple, set)))
        self.assertEqual(len(cabwise), 1)

        cab = cabwise[0]
        self.assertTrue(isinstance(cab, tfl.Cabwise))
        self.assertIn("Minicab", cab.OperatorTypes)

    def test_journey_mode(self):
        api = tfl.Api(app_id=self.app_id, app_key=self.app_key)
        modes = api.GetJourneyModes()
        self.assertGreater(len(modes), 0)
        self.assertTrue(isinstance(modes[0], tfl.JourneyMode))
