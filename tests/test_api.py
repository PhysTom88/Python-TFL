import unittest

from tfl.api import Api
from tfl.api.exceptions import TflError

class TestApi(unittest.TestCase):

    def test_api_all_credentials(self):
        api = Api(app_id="test_id", app_key="test_key", timeout=5)
        self.assertEqual(api.app_id, "test_id")
        self.assertEqual(api.app_key, "test_key")
        self.assertEqual(api.timeout, 5)

    def test_api_missing_credentials(self):
        self.assertRaises(TflError, Api, app_key="Test_key")