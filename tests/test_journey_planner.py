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

    @responses.activate
    def test_journey_planner_diambiguation(self):
        with open("tests/testdata/journey/planner_disambiguation.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        journey = self.api.SearchJourneyPlanner(
            _from="Euston", to="Kings Cross"
        )

        self.assertTrue(isinstance(journey, tfl.JourneyDisambiguation))
        self.assertTrue(isinstance(
            journey.toLocationDisambiguation,
            tfl.models.LocationDisambiguation)
        )
        self.assertTrue(isinstance(
            journey.toLocationDisambiguation.disambiguationOptions, list)
        )
        self.assertTrue(isinstance(
            journey.toLocationDisambiguation.disambiguationOptions[0],
            tfl.models.DisambiguationOption)
        )
        self.assertTrue(isinstance(
            journey.fromLocationDisambiguation,
            tfl.models.LocationDisambiguation)
        )
        self.assertTrue(isinstance(
            journey.fromLocationDisambiguation.disambiguationOptions, list)
        )
        self.assertTrue(isinstance(
            journey.fromLocationDisambiguation.disambiguationOptions[0],
            tfl.models.DisambiguationOption)
        )
        self.assertTrue(isinstance(
            journey.viaLocationDisambiguation,
            tfl.models.LocationDisambiguation)
        )
        self.assertEqual(
            journey.viaLocationDisambiguation.disambiguationOptions,
            None
        )
        self.assertTrue(isinstance(
            journey.searchCriteria, tfl.models.JourneySearch)
        )
        self.assertTrue(isinstance(
            journey.recommendedMaxAgeMinutes, int)
        )
        self.assertTrue(isinstance(
            journey.journeyVector, tfl.models.JourneyOutline)
        )

    @responses.activate
    def test_journey_planner_default(self):
        with open("tests/testdata/journey/planner_default.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        journey = self.api.SearchJourneyPlanner(_from="1000129", to="1000077")

        self.assertTrue(isinstance(journey, tfl.JourneyPlanner))
        self.assertTrue(isinstance(journey.journeys, list))
        self.assertTrue(isinstance(journey.journeys[0], tfl.models.Journey))
        self.assertTrue(isinstance(journey.lines, list))
        self.assertTrue(isinstance(journey.lines[0], tfl.models.Line))
        self.assertTrue(isinstance(
            journey.searchCriteria, tfl.models.JourneySearch)
        )
        self.assertTrue(isinstance(
            journey.recommendedMaxAgeMinutes, int)
        )
        self.assertTrue(isinstance(
            journey.journeyVector, tfl.models.JourneyOutline)
        )

    @responses.activate
    def test_journey_planner_via(self):
        with open("tests/testdata/journey/planner_via.json") as f:
            json_data = f.read()

        responses.add(
            responses.GET, DEFAULT_URL, body=json_data,
            match_querystring=True
        )

        journey = self.api.SearchJourneyPlanner(
            _from="1000129", to="1000077", via="1000248"
        )

        self.assertTrue(isinstance(journey, tfl.JourneyPlanner))
        self.assertTrue(isinstance(journey.journeys, list))
        self.assertTrue(isinstance(journey.journeys[0], tfl.models.Journey))
        self.assertTrue(isinstance(journey.lines, list))
        self.assertTrue(isinstance(journey.lines[0], tfl.models.Line))
        self.assertTrue(isinstance(
            journey.searchCriteria, tfl.models.JourneySearch)
        )
        self.assertTrue(isinstance(
            journey.recommendedMaxAgeMinutes, int)
        )
        self.assertTrue(isinstance(
            journey.journeyVector, tfl.models.JourneyOutline)
        )
        self.assertEqual(journey.journeyVector.to, "1000077")
        self.assertEqual(journey.journeyVector._from, "1000129")
        self.assertEqual(journey.journeyVector.via, "1000248")
