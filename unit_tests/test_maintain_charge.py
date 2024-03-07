import pytest
from flask import json
from local_land_charges_api_stub.main import app
import unittest

class TestMaintainCharge(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add_charge_successful(self):
        """Test adding a charge successfully."""
        payload = {
            "item": {
                "schema-version": "5.0",
                "further-information-location": "some further info",
                "charge-type": "Planning",
                "charge-sub-category": "Conservation area",
                "expiry-date": "2020-01-01",
                "originating-authority": "Place City Council",
                "charge-creation-date": "2017-01-12",
                "geometry": {
                "type": "FeatureCollection",
                "features": [
                    {
                    "geometry": {
                        "coordinates": [
                        294300,
                        21054
                        ],
                        "type": "Point"
                    },
                    "crs": {
                        "type": "name1",
                        "properties": {
                        "name": "urn:ogc:def:crs:EPSG::27700"
                        }
                    },
                    "type": "Feature",
                    "properties": {
                        "id": 410
                    }
                    }
                ]
                },
                "statutory-provision": "Town and Country Planning Act 1990",
                "further-information-reference": "AB1212",
                "instrument": "Notice",
                "charge-geographic-description": "Varying as LR user",
                "supplementary-information": "a description of the local land charge"
            }
        }

        response = self.client.post('/v1.0/local-land-charges', json=payload, content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 201
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'land-charge-id' in data

    def test_add_charge_validation_error(self):
        """Test adding a charge with validation errors."""
        payload = {
            "item": {
                "schema-version": "5.0",
                "further-information-location": "some further info",
                "charge-type": "wrong charge type",
                "charge-sub-category": "Conservation area",
                "expiry-date": "2020-01-01",
                "originating-authority": "Place City Council",
                "charge-creation-date": "2017-01-12",
                "geometry": {
                "type": "FeatureCollection",
                "features": [
                    {
                    "geometry": {
                        "coordinates": [
                        294300,
                        21054
                        ],
                        "type": "Point"
                    },
                    "crs": {
                        "type": "name1",
                        "properties": {
                        "name": "urn:ogc:def:crs:EPSG::27700"
                        }
                    },
                    "type": "Feature",
                    "properties": {
                        "id": 410
                    }
                    }
                ]
                },
                "statutory-provision": "Town and Country Planning Act 1990",
                "further-information-reference": "AB1212",
                "instrument": "Notice",
                "charge-geographic-description": "Varying as LR user",
                "supplementary-information": "a description of the local land charge"
            }
        }
        response = self.client.post('/v1.0/local-land-charges', json=payload, content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 400
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'error_message' in data
        assert 'error' in data['error_message']
        assert data['error_message']['error'] == 'Charge is invalid'


    def test_add_missing_field_error(self):
        """Test adding a charge with validation errors."""
        payload = {
            "item": {
                "schema-version": "5.0",
                "further-information-location": "some further info",
                "charge-sub-category": "Conservation area",
                "expiry-date": "2020-01-01",
                "originating-authority": "Place City Council",
                "charge-creation-date": "2017-01-12",
                "geometry": {
                "type": "FeatureCollection",
                "features": [
                    {
                    "geometry": {
                        "coordinates": [
                        294300,
                        21054
                        ],
                        "type": "Point"
                    },
                    "crs": {
                        "type": "name1",
                        "properties": {
                        "name": "urn:ogc:def:crs:EPSG::27700"
                        }
                    },
                    "type": "Feature",
                    "properties": {
                        "id": 410
                    }
                    }
                ]
                },
                "statutory-provision": "Town and Country Planning Act 1990",
                "further-information-reference": "AB1212",
                "instrument": "Notice",
                "charge-geographic-description": "Varying as LR user",
                "supplementary-information": "a description of the local land charge"
            }
        }
        response = self.client.post('/v1.0/local-land-charges', json=payload, content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 400
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'error_code' in data
        assert data['error_code'] == 'E100'


    def test_add_charge_duplicate(self):
        """Test adding a charge that is detected as a duplicate."""
        payload = {
            "item": {
                "schema-version": "5.0",
                "further-information-location": "some further info",
                "charge-type": "Planning",
                "charge-sub-category": "Conservation area",
                "expiry-date": "2020-01-01",
                "originating-authority": "Place City Council",
                "charge-creation-date": "2017-01-12",
                "geometry": {
                "type": "FeatureCollection",
                "features": [
                    {
                    "geometry": {
                        "coordinates": [
                        294300,
                        21054
                        ],
                        "type": "Point"
                    },
                    "crs": {
                        "type": "name1",
                        "properties": {
                        "name": "urn:ogc:def:crs:EPSG::27700"
                        }
                    },
                    "type": "Feature",
                    "properties": {
                        "id": 410
                    }
                    }
                ]
                },
                "statutory-provision": "Town and Country Planning Act 1990",
                "further-information-reference": "AB1212",
                "instrument": "Notice",
                "charge-geographic-description": "Varying as LR user",
                "supplementary-information": "DUPLICATE"
            }
        }
        response = self.client.post('/v1.0/local-land-charges', json=payload, content_type='application/json', headers={'Accept': 'application/json'})
        assert response.status_code == 409
        assert 'application/json' in response.content_type
        data = json.loads(response.data)
        assert 'duplicate_charges' in data


    def test_vary_charge_valid(self):
        valid_land_charge_id = "LLC-01"
        valid_version_id = "1"
        payload = {
            "item": {
                "schema-version": "5.0",
                "further-information-location": "some further info",
                "charge-type": "Planning",
                "charge-sub-category": "Conservation area",
                "expiry-date": "2020-01-01",
                "originating-authority": "Place City Council",
                "charge-creation-date": "2017-01-12",
                "geometry": {
                "type": "FeatureCollection",
                "features": [
                    {
                    "geometry": {
                        "coordinates": [
                        294300,
                        21054
                        ],
                        "type": "Point"
                    },
                    "crs": {
                        "type": "name1",
                        "properties": {
                        "name": "urn:ogc:def:crs:EPSG::27700"
                        }
                    },
                    "type": "Feature",
                    "properties": {
                        "id": 410
                    }
                    }
                ]
                },
                "statutory-provision": "Town and Country Planning Act 1990",
                "further-information-reference": "AB1212",
                "instrument": "Notice",
                "charge-geographic-description": "Varying as LR user",
                "supplementary-information": "a description of the local land charge"
            }
        }

        response = self.client.put(
            f"/v1.0/local-land-charges/{valid_land_charge_id}/{valid_version_id}",
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 201)

    def test_vary_charge_invalid_land_charge_id(self):
        invalid_land_charge_id = "invalid123" 
        valid_version_id = "1"
        payload = {
            "item": {
                "schema-version": "5.0",
                "further-information-location": "some further info",
                "charge-type": "Planning",
                "charge-sub-category": "Conservation area",
                "expiry-date": "2020-01-01",
                "originating-authority": "Place City Council",
                "charge-creation-date": "2017-01-12",
                "geometry": {
                "type": "FeatureCollection",
                "features": [
                    {
                    "geometry": {
                        "coordinates": [
                        294300,
                        21054
                        ],
                        "type": "Point"
                    },
                    "crs": {
                        "type": "name1",
                        "properties": {
                        "name": "urn:ogc:def:crs:EPSG::27700"
                        }
                    },
                    "type": "Feature",
                    "properties": {
                        "id": 410
                    }
                    }
                ]
                },
                "statutory-provision": "Town and Country Planning Act 1990",
                "further-information-reference": "AB1212",
                "instrument": "Notice",
                "charge-geographic-description": "Varying as LR user",
                "supplementary-information": "a description of the local land charge"
            }
        }


        response = self.client.put(
            f"/v1.0/local-land-charges/{invalid_land_charge_id}/{valid_version_id}",
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 422)

    def test_vary_charge_invalid_version_id(self):
        valid_land_charge_id = "LLC-01"
        invalid_version_id = "abc"
        payload = {
                "item": {
                    "schema-version": "5.0",
                    "further-information-location": "some further info",
                    "charge-type": "Planning",
                    "charge-sub-category": "Conservation area",
                    "expiry-date": "2020-01-01",
                    "originating-authority": "Place City Council",
                    "charge-creation-date": "2017-01-12",
                    "geometry": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                        "geometry": {
                            "coordinates": [
                            294300,
                            21054
                            ],
                            "type": "Point"
                        },
                        "crs": {
                            "type": "name1",
                            "properties": {
                            "name": "urn:ogc:def:crs:EPSG::27700"
                            }
                        },
                        "type": "Feature",
                        "properties": {
                            "id": 410
                        }
                        }
                    ]
                    },
                    "statutory-provision": "Town and Country Planning Act 1990",
                    "further-information-reference": "AB1212",
                    "instrument": "Notice",
                    "charge-geographic-description": "Varying as LR user",
                    "supplementary-information": "a description of the local land charge"
                }
            }


        response = self.client.put(
            f"/v1.0/local-land-charges/{valid_land_charge_id}/{invalid_version_id}",
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 422)
