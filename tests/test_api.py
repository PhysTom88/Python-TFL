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

    @responses.activate
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

    @responses.activate
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

    @responses.activate
    def test_air_quality(self):
        with open("tests/testdata/air_quality.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        air_quality = self.api.GetAirQuality()

        self.assertEqual(len(air_quality), 2)
        self.assertTrue(isinstance(air_quality[0], tfl.AirQuality))

    @responses.activate
    def test_bike_points(self):
        with open("tests/testdata/bike_points.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        bike_points = self.api.GetBikePoints()
        self.assertTrue(isinstance(bike_points, (list, tuple, set)))
        self.assertGreater(len(bike_points), 0)

        bike_point = bike_points[0]
        self.assertTrue(isinstance(bike_point, tfl.Point))
        self.assertGreater(len(bike_point.additionalProperties), 0)
        self.assertTrue(isinstance(
            bike_point.additionalProperties[0], tfl.AdditionalProperty)
        )

    @responses.activate
    def test_bike_point_correct(self):
        with open("tests/testdata/bike_point_correct.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        bike_point = self.api.GetBikePoint("BikePoints_76")

        self.assertTrue(isinstance(bike_point, tfl.Point))
        self.assertGreater(len(bike_point.additionalProperties), 0)
        self.assertTrue(isinstance(
            bike_point.additionalProperties[0], tfl.AdditionalProperty)
        )

    @responses.activate
    def test_bike_point_incorrect(self):
        with open("tests/testdata/bike_point_incorrect.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        self.assertRaises(
            tfl.TflError, lambda: self.api.GetBikePoint("Invalid_BikePoint")
        )

    @responses.activate
    def test_bike_point_search_correct(self):
        with open("tests/testdata/bike_point_search_correct.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        bike_points = self.api.SearchBikePoints("St James")
        self.assertTrue(isinstance(bike_points, (list, tuple, set)))
        self.assertGreater(len(bike_points), 0)

        bike_point = bike_points[0]
        self.assertTrue(isinstance(bike_point, tfl.Point))

    @responses.activate
    def test_bike_point_search_invalid(self):
        with open("tests/testdata/bike_point_search_invalid.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        bike_points = self.api.SearchBikePoints("Nowhere in London")
        self.assertEqual(len(bike_points), 0)

    @responses.activate
    def test_cabwise_correct_no_options(self):
        with open("tests/testdata/cabwise_no_options.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        cabwise = self.api.SearchCabwise(lat=51.5033, lon=-0.12763)
        self.assertTrue(isinstance(cabwise, (list, tuple, set)))
        self.assertGreater(len(cabwise), 0)

        cab = cabwise[0]
        self.assertTrue(isinstance(cab, tfl.Cabwise))

    @responses.activate
    def test_cabwise_correct_extra_params(self):
        with open("tests/testdata/cabwise_extra_options.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        cabwise = self.api.SearchCabwise(
            lat=51.5033, lon=-0.12763, optype="Minicab",
            radius=2000, maxResults=1)
        self.assertTrue(isinstance(cabwise, (list, tuple, set)))
        self.assertEqual(len(cabwise), 1)

        cab = cabwise[0]
        self.assertTrue(isinstance(cab, tfl.Cabwise))
        self.assertIn("Minicab", cab.OperatorTypes)

    @responses.activate
    def test_journey_mode(self):
        with open("tests/testdata/journey_mode.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        modes = self.api.GetJourneyModes()
        self.assertGreater(len(modes), 0)
        self.assertTrue(isinstance(modes[0], tfl.JourneyMode))

    @responses.activate
    def test_line_mode(self):
        with open("tests/testdata/line_mode.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        modes = self.api.GetLineModes()
        self.assertGreater(len(modes), 0)
        self.assertTrue(isinstance(modes[0], tfl.JourneyMode))

    @responses.activate
    def test_line_severity_codes(self):
        with open("tests/testdata/line_severity_codes.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        codes = self.api.GetLineSeverityCodes()
        self.assertTrue(isinstance(codes, list))
        self.assertGreater(len(codes), 1)
        self.assertTrue(isinstance(codes[0], tfl.LineStatusSeverity))

    @responses.activate
    def test_line_disruption_category(self):
        with open("tests/testdata/line_disruption_category.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        categories = self.api.GetLineDisruptionCategories()
        self.assertTrue(isinstance(categories, list))
        self.assertGreater(len(categories), 1)
        self.assertTrue(isinstance(categories[0], unicode))

    @responses.activate
    def test_line_service_types(self):
        with open("tests/testdata/line_service_types.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        services = self.api.GetLineServiceTypes()
        self.assertTrue(isinstance(services, list))
        self.assertGreater(len(services), 1)
        self.assertTrue(isinstance(services[0], unicode))

    @responses.activate
    def test_line_by_id(self):
        with open("tests/testdata/line_by_id.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        lines = self.api.GetLines(["bakerloo", "central"])
        self.assertTrue(isinstance(lines, list))
        self.assertTrue(len(lines), 2)
        self.assertTrue(isinstance(lines[0], tfl.Line))
