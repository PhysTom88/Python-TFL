import json
import unittest

import tfl


class AirQualityTest(unittest.TestCase):
    FORECAST_SUMMARY = """Moderate air pollution forecast valid from Wednesday 21 February to end of Wednesday 21 February GMT"""

    FORECAST_TEXT = """The latest pollution measurements show a build up..."""
    SAMPLE_JSON = '''{"sO2Band": "Low", "forecastText": "The latest pollution measurements show a build up...", "$id": "2", "$type": "Tfl.Api.Presentation.Entities.CurrentForecast, Tfl.Api.Presentation.Entities", "forecastBand": "Moderate", "pM25Band": "Moderate", "forecastType": "Current", "pM10Band": "Moderate", "forecastID": "13838", "o3Band": "Low", "forecastSummary": "Moderate air pollution forecast valid from Wednesday 21 February to end of Wednesday 21 February GMT", "nO2Band": "Low"}'''

    def _SampleAirQuality(self):
        return tfl.AirQuality(
            forecastType="Current",
            forecastID="13838",
            forecastBand="Moderate",
            forecastSummary=self.FORECAST_SUMMARY,
            nO2Band="Low",
            o3Band="Low",
            pM10Band="Moderate",
            pM25Band="Moderate",
            sO2Band="Low",
            forecastText=self.FORECAST_TEXT
        )

    def test_parameters(self):
        air_quality = tfl.AirQuality()
        air_quality.forecastType = "Current"
        self.assertEqual("Current", air_quality.forecastType)

        air_quality.forecastID = "13838"
        self.assertEqual("13838", air_quality.forecastID)

        air_quality.forecastBand = "Moderate"
        self.assertEqual("Moderate", air_quality.forecastBand)

        air_quality.forecastSummary = self.FORECAST_SUMMARY
        self.assertEqual(self.FORECAST_SUMMARY, air_quality.forecastSummary)

        air_quality.nO2Band = "Low"
        self.assertEqual("Low", air_quality.nO2Band)

        air_quality.o3Band = "Low"
        self.assertEqual("Low", air_quality.o3Band)

        air_quality.p10Band = "Moderate"
        self.assertEqual("Moderate", air_quality.p10Band)

        air_quality.p25Band = "Moderate"
        self.assertEqual("Moderate", air_quality.p25Band)

        air_quality.sO2Band = "Low"
        self.assertEqual("Low", air_quality.sO2Band)

        air_quality.forecastText = self.FORECAST_TEXT
        self.assertEqual(self.FORECAST_TEXT, air_quality.forecastText)

    def test_to_dict(self):
        air_quality = self._SampleAirQuality()
        data = air_quality.toDict()
        self.assertEqual("Current", data["forecastType"])
        self.assertEqual("13838", data["forecastID"])
        self.assertEqual("Moderate", data["forecastBand"])
        self.assertEqual(self.FORECAST_SUMMARY, data["forecastSummary"])
        self.assertEqual("Low", data["nO2Band"])
        self.assertEqual("Low", data["o3Band"])
        self.assertEqual("Moderate", data["pM10Band"])
        self.assertEqual("Moderate", data["pM25Band"])
        self.assertEqual("Low", data["sO2Band"])
        self.assertEqual(self.FORECAST_TEXT, data["forecastText"])

    def test_from_json(self):
        data = json.loads(self.SAMPLE_JSON)
        air_quality = tfl.AirQuality.fromJSON(data)
        self.assertEqual(self._SampleAirQuality(), air_quality)
