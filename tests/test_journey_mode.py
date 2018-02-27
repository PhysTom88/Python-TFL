import json
import unittest

import tfl


class JourneyModeTest(unittest.TestCase):

	SAMPLE_JSON = '''{"isTflService": false, "isFarePaying": true, "isScheduledService": false, "modeName": "black-cab-as-customer"}'''

	def _SampleJourneyMode(self):
		return tfl.JourneyMode(
			isTflService=False,
			isFarePaying=True,
			isScheduledService=False,
			modeName="black-cab-as-customer"
		)

	def test_parameters(self):
		journey_mode = tfl.JourneyMode()
		journey_mode.isTflService=False
		self.assertEqual(False, journey_mode.isTflService)

		journey_mode.isFarePaying=True
		self.assertEqual(True, journey_mode.isFarePaying)

		journey_mode.isScheduledService=False
		self.assertEqual(False, journey_mode.isScheduledService)

		journey_mode.modeName="black-cab-as-customer"
		self.assertEqual("black-cab-as-customer", journey_mode.modeName)

	def test_to_dict(self):
		journey_mode = self._SampleJourneyMode()
		data = journey_mode.toDict()

		self.assertEqual(False, data["isTflService"])
		self.assertEqual(True, data["isFarePaying"])
		self.assertEqual(False, data["isScheduledService"])
		self.assertEqual("black-cab-as-customer", data["modeName"])

	def test_from_json(self):
		data = json.loads(self.SAMPLE_JSON)
		journey_mode = tfl.JourneyMode.fromJSON(data)
		self.assertEqual(self._SampleJourneyMode(), journey_mode)
