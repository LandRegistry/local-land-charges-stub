# Third party Local Land Charges API stub service
The stub service is a stand-a-lone service without any database connectivity or reliance on other service API's.
It is developed to return responses to replicate a live service, in many cases these are static files that are returned.
It is intended as a tool for third party users to develop services to use the Local Land Charge API. 

This is currently a Beta version and therefore subject to future changes.

## Getting Started

Running this service locally will require the following :
* Python 3.9 - 3.10.10
* Python 3 header files and a static library for Python (`python3-dev` on Debian/ Ubuntu)

To start the service, run the ```./run.sh``` file in Termina;.
If using Windows, run the ```./run_in_windows.bat``` file in a cmd window. 

You may need to update the bat file code to use py or python3, instead of python, depending on your PATH configuration.

Check application is running using http://localhost:9998/health

The base URL for the application will run on http://localhost:9998/v1.0/local-land-charges (See swagger documentation for details of the available endpoints)

The following provides information on available data and responses.

## Retrieve a Local Land Charge
* land-charge-id is LLC-1, response is "basic Local Land Charge response"
* land-charge-id is LLC-2, response is "No charge found response"
* land-charge-id is CLL-3, response is "Invalid format for charge ID"
* land-charge-id is LLC-4, response is "Minimum return fields for returned Local Land Charge"
* land-charge-id is LLC-5, response is "Maximum return fields for returned Local Land Charge"
* land-charge-id is LLC-6, response is "S52 Land Compensation Charge"
* land-charge-id is LLC-7, response is "S8 Land Compensation Charge"
* land-charge-id is LLC-8, response is "Specific Financial Charge"
* land-charge-id is LLC-9, response is "Light Obstruction Notice"
* any other Land Charge ID will return same as for LLC-1



## Add a Local Land Charge
Requires a valid JSON/Payload for the POST request. See swagger documentation for more details.
i.e.
```
{
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
```

The service will validate against the JSON schema for mandatory elements. Omitting a mandatory element i.e. charge-type will return an error response, example below
```
{
    "error_message": {
        "error": "Charge is invalid",
        "details": [
            {
                "location": "$.",
                "error_message": "'charge-type' is a required property"
            }
        ]
    },
    "error_code": "E100"
}
```

The service will also validate the supplied charge categories, sub-categories, and instruments. This validation will be applied against a dictionary object found in /local_land_charges_api_stub/validation/categories.py and list of instruments in instruments/py  

The live service will check whether a charge being added is a duplicate that is already held. To recreate the response for this scenario set the value of "supplementary-information" in the request JSON payload to "DUPLICATE". The response will return a 409 HTTP code with this example message
```
{
    "duplicate_charges": [
        "LLC-D"
    ]
}
```


## Vary and cancel Local Land Charge
For Vary, use any valid JSON/Payload as for 'Add Local Land Charge' example above.
The following params can be used for both vary and cancel (no JSON/Payload required for cancel):

*  land-charge-id=LLC-10, version-id=3, Response="ID 'LLC-10' cannot be found", status_code 404, see Example 1 below

*  land-charge-id=LLC-10, version-id=anything but 3, Response="Version ID submitted is not latest version", status_code 422, see Example 2 below

*  land-charge-id=LLC-99, version-id=any integer value(no decimals), Response="Cannot amend a cancelled record", status_code 400, see Example 3 below

*  any other valid params returns a good response

### Example 1
```
{
    "error_code": 404,
    "error_message": "ID 'LLC-10' cannot be found"
}
```

### Example 2
```
{
    "error_code": "E010",
    "error_message": "Version ID submitted is not latest version"
}
```

### Example 3
```
{
    "error_code": "E400",
    "error_message": {
        "details": [{
            "location": "$.item.end-date",
            "error_message": "Cannot amend a cancelled record"
        }],
        "error": "Charge is invalid"
    }
}
```

## Swagger
To run the premade swagger server, move to the directory /Swagger, then execute the command 'python3 pythonserver.py'
Open your favourite web browser and go to localhost:8000
If the api is running the UI will be able to send payloads to it.

The schema file the swagger uses can be found at /Swagger/Swagger.json.
If you wish to update the schema you may want to convert the /local_land_charges_api_stub/documentation/local-land-charges-api.yml file to json and replace the swagger.json with it.

## Testing
To run the tests, if on Windows, run ```./run_tests_in_windows.bat``` in the Oerminal.

Otherwise run the ```./run_tests.sh``` file in Terminal

## NOTE:
The following link contains the list of Statutory Provisions are available to use in this stub:-

https://search-local-land-charges.service.gov.uk/statutory-provisions
