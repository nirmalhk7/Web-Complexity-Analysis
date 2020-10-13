# # Characterizing Webpage Complexity and Its Impact

import csv
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from prettytable import PrettyTable
import json
from browsermobproxy import Server
# https://dzone.com/articles/performance-capture-i-export-har-using-selenium-an



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
        self.requests_per_second= 0

"""Delete previous screenshots and har_data"""
os.system("rm -rf screenshots/*")
os.system("rm -rf har_data/*")


"""Read CSV file"""
with open('dataset.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        data.append(websiteDetails(row["name"],int(row["rank"])))
        line_count += 1

"""Start browsermob-proxy server"""
# https://stackoverflow.com/questions/48201944/how-to-use-browsermob-with-python-selenium
server_port=8090
server= Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy",options={'port':server_port})
server.start()
proxy= server.create_proxy()
print("browsermob-proxy active on {}".format(server_port))


"""Set options for Chrome browser"""
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('ignore-certificate-errors')
options.add_argument("--proxy-server={}".format(proxy.proxy))
driver = webdriver.Chrome(chrome_options=options)


SIZE = 5
for i in range(SIZE):
    elem= data[i]
    print("Testing for",elem.name)
    try:
        elem.reqcode= requests.get("https://www."+elem.name).status_code
    except:
        elem.reqcode="N/A"
        continue
    if(200<=elem.reqcode<300):
        print("Opening ",elem.name)
        proxy.new_har(elem.name)
        driver.get('https://www.'+elem.name)
        
        with open('har_data/'+elem.name+'.har','w') as har_file:
            json.dump(proxy.har,har_file)

driver.quit();
server.stop();
# driver.close();
table= PrettyTable(['Website Name',"Request Code"])
for i in data[:SIZE]:
    table.add_row([i.name,i.reqcode])
print(table)
