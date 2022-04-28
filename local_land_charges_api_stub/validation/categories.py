import json
import time
import requests


class Categories(object):
    
    def get_category_data(self):
        url = 'https://search-local-land-charges.service.gov.uk/categories/all'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/605.1.15'}
        response = requests.get(url, headers=headers)
        category_dict=self.organise_category_list(json.loads(response.content))
        return category_dict

    def organise_category_list(self, category_data):
        full_category_dict={}

        for category_type in category_data:
            if category_type.get("name") != None:
                category_dict={}
                if category_type.get("sub-categories", []) != []:
                    category_dict["sub-categories"]={}
                    for sub_category in category_type.get("sub-categories", []):
                        sub_categories={
                            sub_category.get("name"):{}
                        }                        
                        if sub_category.get("instruments",[]) != []:
                            
                            sub_categories[sub_category["name"]].update({
                                    "instruments":sub_category.get("instruments",[])
                                     })
                    
                        category_dict["sub-categories"].update(sub_categories)

                full_category_dict[category_type.get("name")]=category_dict

        return full_category_dict
