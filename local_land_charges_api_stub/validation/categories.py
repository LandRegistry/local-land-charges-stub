import json
import requests


class Categories(object):

    def get_category_data(self):
        url = 'https://search-local-land-charges.service.gov.uk/categories/all'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/605.1.15'}
        response = requests.get(url, headers=headers)
        try:
            category_data = json.loads(response.content)
        except json.JSONDecodeError:
            with open('local_land_charges_api_stub/constants/categories.json') as category_dict:
                category_data = json.loads(category_dict.read())

        return self.organise_category_list(category_data)

    def organise_category_list(self, category_data):
        full_category_dict = {}

        for category_type in category_data:
            if category_type.get("name") is not None:
                category_dict = {}
                if category_type.get("sub-categories", []) != []:
                    category_dict["sub-categories"]={}
                    for sub_category in category_type.get("sub-categories", []):
                        sub_categories = {
                            sub_category.get("name"):{}
                        }
                        if sub_category.get("instruments",[]) != []:

                            sub_categories[sub_category["name"]].update({
                                    "instruments": sub_category.get("instruments", [])
                                     })

                        category_dict["sub-categories"].update(sub_categories)

                full_category_dict[category_type.get("name")]=category_dict

        return full_category_dict
