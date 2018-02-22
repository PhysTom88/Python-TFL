
import calendar
import json
import unittest

import tfl


class AccidentStatTest(unittest.TestCase):

    SAMPLE_JSON = '''{"id": 269639, "lat": 51.5169, "lon": -0.1428, "date": "2016-06-04T20:00:00Z", "severity": "Slight", "borough": "City of Westminster"}'''

    def _SampleAccident(self):
        return tfl.Accident(
            id=269639,
            lat=51.5169,
            lon=-0.1428,
            date="2016-06-04T20:00:00Z",
            severity="Slight",
            borough="City of Westminster"
        )

    def test_parameters(self):
        accident = tfl.Accident()
        accident.id = 269639
        self.assertEqual(269639, accident.id)

        accident.lat = 51.5169
        self.assertEqual(51.5169, accident.lat)

        accident.lon = -0.1428
        self.assertEqual(-0.1428, accident.lon)

        accident.date = "2016-06-04T20:00:00Z"
        date_seconds = calendar.timegm((2016, 6, 4, 20, 0, 0, -1, -1, -1))
        self.assertEqual("2016-06-04T20:00:00Z", accident.date)
        self.assertEqual(date_seconds, accident.date_in_seconds)

        accident.severity = "Slight"
        self.assertEqual("Slight", accident.severity)

        accident.borough = "City of Westminster"
        self.assertEqual("City of Westminster", accident.borough)

    def test_to_dict(self):
        accident = self._SampleAccident()
        data = accident.toDict()
        self.assertEqual(269639, data["id"])
        self.assertEqual(51.5169, data["lat"])
        self.assertEqual(-0.1428, data["lon"])
        self.assertEqual("2016-06-04T20:00:00Z", data["date"])
        self.assertEqual("Slight", data["severity"])
        self.assertEqual("City of Westminster", data["borough"])

    def test_from_json(self):
        data = json.loads(self.SAMPLE_JSON)
        accident = tfl.Accident.fromJSON(data)
        self.assertEqual(self._SampleAccident(), accident)
