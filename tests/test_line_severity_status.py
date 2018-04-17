import json
import unittest

import tfl


class LineStatusSeverityTest(unittest.TestCase):

    SAMPLE_JSON = '''{"modeName": "cable-car", "severityLevel": 0, "description": "Special Service"}'''

    def _SampleLineStatusSeverity(self):
        return tfl.LineStatusSeverity(
            modeName="cable-car",
            severityLevel=0,
            description="Special Service"
        )

    def test_parameters(self):
        severity = tfl.LineStatusSeverity()
        severity.modeName = "cable-car"
        self.assertEqual("cable-car", severity.modeName)

        severity.severityLevel = 0
        self.assertEqual(0, severity.severityLevel)

        severity.description = "Special Service"
        self.assertEqual("Special Service", severity.description)

    def test_to_dict(self):
        severity = self._SampleLineStatusSeverity()
        data = severity.toDict()
        self.assertEqual("cable-car", data["modeName"])
        self.assertEqual(0, data["severityLevel"])
        self.assertEqual("Special Service", data["description"])

    def test_from_json(self):
        data = json.loads(self.SAMPLE_JSON)
        severity = tfl.LineStatusSeverity.fromJSON(data)
        self.assertEqual(self._SampleLineStatusSeverity(), severity)
