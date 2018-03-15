
import os
import re
import unittest
import responses

import tfl


DEFAULT_URL = re.compile(r'https?://.*\.tfl.gov.uk/.*')


class JourneyResultsDisambiguationTest(unittest.TestCase):

    def setUp(self):
        self.app_id = os.environ.get("APP_ID")
        self.app_key = os.environ.get("APP_KEY")
        self.api = tfl.Api(app_id=self.app_id, app_key=self.app_key)

    @responses.activate
    def test_journey_valid_input(self):
        with open("tests/testdata/journey_disambiguation.json") as f:
            resp_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=resp_data,
            match_querystring=True)

        resp = self.api.SearchJourneyPlanner(
            _from="Kings Cross", to="Hammersmith"
        )

        self.assertTrue(isinstance(resp, tfl.JourneyDisambiguation))
        self.assertTrue(isinstance(
            resp.toLocationDisambiguation, tfl.models.LocationDisambiguation)
        )
        self.assertTrue(isinstance(
            resp.toLocationDisambiguation.disambiguationOptions, list)
        )
        self.assertTrue(isinstance(
            resp.toLocationDisambiguation.disambiguationOptions[0],
            tfl.models.DisambiguationOption)
        )
        self.assertTrue(isinstance(
            resp.fromLocationDisambiguation, tfl.models.LocationDisambiguation)
        )
        self.assertTrue(isinstance(
            resp.fromLocationDisambiguation.disambiguationOptions, list)
        )
        self.assertTrue(isinstance(
            resp.fromLocationDisambiguation.disambiguationOptions[0],
            tfl.models.DisambiguationOption)
        )
        self.assertTrue(isinstance(
            resp.viaLocationDisambiguation, tfl.models.LocationDisambiguation)
        )
        self.assertEqual(
            resp.viaLocationDisambiguation.disambiguationOptions,
            None
        )
        self.assertTrue(isinstance(
            resp.searchCriteria, tfl.models.JourneySearch)
        )
        self.assertTrue(isinstance(
            resp.recommendedMaxAgeMinutes, int)
        )
        self.assertTrue(isinstance(
            resp.journeyVector, tfl.models.JourneyOutline)
        )


class JourneyResultsTest(unittest.TestCase):

    def setUp(self):
        self.app_id = os.environ.get("APP_ID")
        self.app_key = os.environ.get("APP_KEY")
        self.api = tfl.Api(app_id=self.app_id, app_key=self.app_key)

    @responses.activate
    def test_journey_valid_input(self):
        with open("tests/testdata/journey_planner.json") as f:
            resp_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=resp_data,
            match_querystring=True)

        resp = self.api.SearchJourneyPlanner(
            _from="", to=""
        )

        self.assertTrue(isinstance(resp, tfl.JourneyPlanner))
        self.assertTrue(isinstance(resp.journeys, list))
        self.assertTrue(isinstance(resp.journeys[0], tfl.models.Journey))
        self.assertTrue(isinstance(resp.lines, list))
        self.assertTrue(isinstance(resp.lines[0], tfl.models.Line))
        self.assertTrue(isinstance(
            resp.searchCriteria, tfl.models.JourneySearch)
        )
        self.assertTrue(isinstance(
            resp.recommendedMaxAgeMinutes, int)
        )
        self.assertTrue(isinstance(
            resp.journeyVector, tfl.models.JourneyOutline)
        )
