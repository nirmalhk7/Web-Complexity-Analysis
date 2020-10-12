# # Characterizing Webpage Complexity and Its Impact

import csv
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import os

data=[]
class websiteDetails:
    def __init__(self,name,rank):
        self.name=str(name)
        self.rank=int(rank)
        self.category="undefined"
        self.server_count=0
        self.non_origin_count=0

os.system("rm -rf screenshots/*")
with open('dataset.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        data.append(websiteDetails(row["name"],int(row["rank"])))
        line_count += 1


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(options=options)

for i in data[:5]:
    print("Testing for",i.name)
    try:
        driver.get('https://www.'+i.name)
        driver.get_screenshot_as_file('screenshots/'+i.name+'.png')
    except WebDriverException:
        print("Unable to reach "+i.name)
