successful_payload = {
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

invalid_charge_type = {
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

missing_field_payload = {
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

duplicate_charge = {
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

invalid_version = {
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
