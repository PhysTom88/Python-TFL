
import calendar
import json
import unittest

import tfl


class LineByIDTest(unittest.TestCase):

    SAMPLE_JSON = '''{"id": "bakerloo", "name": "Bakerloo", "modeName": "tube", "disruptions": [], "created": "2018-04-12T16:31:47.517Z", "modified": "2018-04-12T16:31:47.517Z", "lineStatuses": [], "routeSections": []}'''

    def _SampleLine(self):
        return tfl.Line(
            id="bakerloo",
            name="Bakerloo",
            modeName="tube",
            disruptions=[],
            created="2018-04-12T16:31:47.517Z",
            modified="2018-04-12T16:31:47.517Z",
            lineStatuses=[],
            routeSections=[]
        )

    def test_parameters(self):
        line = tfl.Line()
        line.id = "bakerloo"
        self.assertEqual("bakerloo", line.id)

        line.name = "Bakerloo"
        self.assertEqual("Bakerloo", line.name)

        line.modeName = "tube"
        self.assertEqual("tube", line.modeName)

        line.created = "2018-04-12T16:31:47.517Z"
        created_seconds = calendar.timegm((2018, 4, 12, 16, 31, 47, 51))
        self.assertEqual("2018-04-12T16:31:47.517Z", line.created)
        self.assertEqual(created_seconds, line.created_in_seconds)

        line.modified = "2018-04-12T16:31:47.517Z"
        modified_seconds = calendar.timegm((2018, 4, 12, 16, 31, 47, 51))
        self.assertEqual("2018-04-12T16:31:47.517Z", line.modified)
        self.assertEqual(modified_seconds, line.modified_in_seconds)

        line.lineStatuses = []
        self.assertEqual([], line.lineStatuses)

    def test_to_dict(self):
        line = self._SampleLine()
        data = line.toDict()
        self.assertEqual("bakerloo", data["id"])
        self.assertEqual("Bakerloo", data["name"])
        self.assertEqual("tube", data["modeName"])
        self.assertEqual("2018-04-12T16:31:47.517Z", data["created"])
        self.assertEqual("2018-04-12T16:31:47.517Z", data["modified"])
        self.assertEqual([], data["lineStatuses"])
        self.assertEqual([], data["routeSections"])

    def test_from_json(self):
        data = json.loads(self.SAMPLE_JSON)
        line = tfl.Line.fromJSON(data)
        self.assertEqual(self._SampleLine(), line)
