from local_land_charges_api_stub.main import app
import unittest


class TestHealth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_health(self):
        self.assertEqual((self.app.get('/health')).status_code, 200)