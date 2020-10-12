# # Characterizing Webpage Complexity and Its Impact

import csv
import requests
from selenium import webdriver
import time

data=[]
class websiteDetails:
    def __init__(self,name,rank):
        self.name=str(name)
        self.rank=int(rank)
        self.category="undefined"
        self.server_count=0
        self.non_origin_count=0


with open('dataset.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        data.append(websiteDetails(row["name"],int(row["rank"])))
        line_count += 1

for i in data[:5]:
    print(i.name)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')


driver = webdriver.Chrome(chrome_options=options)
driver.get('https://'+data[0])
