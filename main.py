# # Characterizing Webpage Complexity and Its Impact

import csv
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from prettytable import PrettyTable


data=[]
class websiteDetails:
    def __init__(self,name,rank):
        self.name=str(name)
        self.rank=int(rank)
        self.category="undefined"
        self.server_count=0
        self.non_origin_count=0
        self.backend_calc=0
        self.frontend_calc=0
        self.reqcode=0

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



SIZE = 5

for i in range(SIZE):
    elem= data[i]
    print("Testing for",elem.name)
    elem.reqcode= requests.get("https://www."+elem.name).status_code
    if(elem.reqcode==200):
        print("Collecting data for",elem.name)
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.'+elem.name)

# https://www.lambdatest.com/blog/how-to-measure-page-load-times-with-selenium/
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")

        elem.backend_calc= responseStart - navigationStart
        elem.frontend_calc= domComplete - responseStart

        driver.get_screenshot_as_file('screenshots/'+elem.name+'.png')
        # driver.quit();
        driver.close();
        # x=int(input())

# driver.close();
table= PrettyTable(['Website Name','Backend RT',"Frontend RT","Request Code"])
for i in data[:SIZE]:
    table.add_row([i.name,i.backend_calc,i.frontend_calc,i.reqcode])
print(table)
