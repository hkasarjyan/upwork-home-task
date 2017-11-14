import unittest
import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

class Freelancer():
    def __init__(self, html_element, freelancer_name, freelancer_title, freelancer_rate, freelancer_earned, freelancer_location, freelancer_description, freelancer_skills):
        self.element = html_element
        self.name=freelancer_name
        self.title=freelancer_title
        self.rate=freelancer_rate
        self.earned=freelancer_earned
        self.location=freelancer_location
        self.description=freelancer_description
        self.skills=freelancer_skills
    
    def getInfo(self):
        print("-----------------Freelancer info------------------\n")
        print("Freelancer Name: %s"%self.name)
        print("Freelancer Title: %s"%self.title)
        print("Freelancer Rate: %s"%self.rate)
        print("Freelancer Earned: %s"%self.earned)
        print("Freelancer Location: %s"%self.location)
        print("Freelancer Description: %s"%self.description)
        print("Freelancer Skills: %s"%self.skills)
    
    def checkValue(self, keyword):
        check=0
        str_skills = ''.join(self.skills)
        checklist = [self.name, self.title, self.location, self.description, str_skills]
        for attribute_value in checklist:        
            if keyword.lower() in attribute_value.lower():
                print("Freelancer with %s name contains search keyword, keyword is in %s attribute"%(self.name, attribute_value))
                check=1
        if check == 0:
            print("Freelancer with %s name does not contain search keyword"%self.name)


class Search(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        
        keyword="armen"
        
        # 2.  Clear `<browser>` cookies
        # Validate cookies are deleted
        driver.delete_all_cookies()
        all_cookies = driver.get_cookies()
        assert all_cookies == []

        # 3.  Go to www.upwork.com
        # Validate upwork.com loads successfully
        driver.get("http://www.upwork.com")
        self.assertIn("Upwork", driver.title)
        
        # 4.  Focus onto "Find freelancers"
        # 5.  Enter `<keyword>` into the search input right from the dropdown
        # and submit it (click on the magnifying glass button)
        # 6.  Select `"Search Anywhere"`
        elem = driver.find_element_by_xpath("//input[@placeholder='Find Freelancers']")
        elem.send_keys(keyword)
        elem.send_keys(Keys.RETURN)
        time.sleep(30)


        # 6.  Parse the 1st page with search results:
        # store info given on the 1st page of search results as structured data
        # of any chosen by you type (i.e.  hash of hashes or array of hashes,
        # whatever structure handy to be parsed).
        elem = driver.find_element_by_id("oContractorResults")
        freelancers_on_page = elem.find_elements_by_xpath("//article[@class='row']")
        freelancers_object_list = []
        for freelancer_element in freelancers_on_page:
            freelancer_name = freelancer_element.find_element_by_xpath(".//a[@class='freelancer-tile-name']")
            freelancer_title = freelancer_element.find_element_by_xpath(".//h4[@class='m-0 freelancer-tile-title ellipsis']")
            freelancer_rates = freelancer_element.find_elements_by_xpath(".//div[@class='col-md-3 p-0-right']")
            freelancer_description = freelancer_element.find_element_by_xpath(".//p[@class='p-0-left m-0 freelancer-tile-description']")
            freelancer_skills = freelancer_element.find_elements_by_xpath(".//a[@class='o-tag-skill m-sm-top m-0-bottom']")
            freelancer_skills_list = []
            for skill in freelancer_skills:
                freelancer_skills_list.append(skill.text)
            freelancers_object_list.append(Freelancer(freelancer_element, freelancer_name.text, freelancer_title.text, freelancer_rates[0].text, freelancer_rates[1].text, freelancer_rates[2].text, freelancer_description.text, freelancer_skills_list))
        
        # 7. Make sure at least one attribute (title, overview, skills, etc) 
           #of each item (found freelancer) from parsed search results contains `<keyword>` 
           #Log in stdout which freelancers and attributes contain `<keyword>` and which do not.
        for freelancer in freelancers_object_list:
            freelancer.checkValue(keyword)

        # 9. Click on random freelancer's title
        # 10. Get into that freelancer's profile
        #generate random number
        random_freelancer_number  = random.randint(0, len(freelancers_object_list)-1)
        freelancer_to_open = freelancers_object_list[random_freelancer_number].element
        freelancer_to_open.click()

        # 11. Check that each attribute value is equal to one of those stored in the structure created in #67
        time.sleep(30)
        elem_freelancer = driver.find_element_by_id("oProfilePage")
        rates=elem_freelancer.find_element_by_class_name("m-lg-top")
        rate = rates.text

        print("AA")





    def tearDown(self):
        print("Exit")
        self.driver.close()

if __name__ == "__main__":
    unittest.main()