import json
import time

from selenium import webdriver
import chromedriver_autoinstaller


class Categories(object):
    
    def get_category_data(self):

        chromedriver_autoinstaller.install()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        browser = webdriver.Chrome(chrome_options=options)

        url = "https://search-local-land-charges.service.gov.uk/categories/all"
        
        browser.get(url)
        time.sleep(3)
        html = browser.execute_script("return document.getElementsByTagName('pre')[0].innerHTML")
        category_dict=self.organise_category_list(json.loads(html))

        browser.close()
        return category_dict

    def organise_category_list(self, category_data):
        full_category_dict={}

        for category_type in category_data:
            if category_type.get("name") != None:
                category_dict={}
                if category_type.get("sub-categories", {}) != {}:
                    category_dict["sub-categories"]={}
                    for sub_category in category_type.get("sub-categories", {}):
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
