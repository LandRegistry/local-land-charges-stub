import pytest
from flask import json
from local_land_charges_api_stub.main import app
from unit_tests.static import test_data
import unittest


class TestMaintainCharge(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add_charge_successful(self):
        """Test adding a charge successfully."""

        response = self.client.post('/v1.0/local-land-charges', json=test_data.successful_payload,
                                    content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 201
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'land-charge-id' in data

    def test_add_charge_validation_error(self):
        """Test adding a charge with validation errors."""
        response = self.client.post('/v1.0/local-land-charges', json=test_data.invalid_charge_type,
                                    content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 400
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'error_message' in data
        assert 'error' in data['error_message']
        assert data['error_message']['error'] == 'Charge is invalid'

    def test_add_missing_field_error(self):
        """Test adding a charge with validation errors."""

        response = self.client.post('/v1.0/local-land-charges', json=test_data.missing_field_payload,
                                    content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 400
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'error_code' in data
        assert data['error_code'] == 'E100'

    def test_add_charge_duplicate(self):
        """Test adding a charge that is detected as a duplicate."""

        response = self.client.post('/v1.0/local-land-charges', json=test_data.duplicate_charge, content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 409
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'duplicate_charges' in data

    def test_vary_charge_valid(self):
        valid_land_charge_id = "LLC-01"
        valid_version_id = "1"

        response = self.client.put(
            f"/v1.0/local-land-charges/{valid_land_charge_id}/{valid_version_id}",
            data=json.dumps(test_data.successful_payload),
            content_type='application/json',
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 201)

    def test_vary_charge_invalid_land_charge_id(self):
        invalid_land_charge_id = "invalid123"
        valid_version_id = "1"

        response = self.client.put(
            f"/v1.0/local-land-charges/{invalid_land_charge_id}/{valid_version_id}",
            data=json.dumps(test_data.invalid_charge_type),
            content_type='application/json',
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 422)

    def test_vary_charge_invalid_version_id(self):
        valid_land_charge_id = "LLC-01"
        invalid_version_id = "abc"

        response = self.client.put(
            f"/v1.0/local-land-charges/{valid_land_charge_id}/{invalid_version_id}",
            data=json.dumps(test_data.invalid_version),
            content_type='application/json',
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 422)
