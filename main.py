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
import argparse
from Website import websiteDetails

parser= argparse.ArgumentParser()
parser.add_argument("-redo", "--regenerate", help="Regenerate HAR files")

args= parser.parse_args()
# https://dzone.com/articles/performance-capture-i-export-har-using-selenium-an

data=[]




"""Delete previous screenshots and har_data"""
os.system("rm -rf screenshots/*")
# if(args.regenerate):
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
        
        with open('har_data/'+elem.name+'-har.json','w') as har_file:
            json.dump(proxy.har,har_file)
        
        jsondata= json.load(open('har_data/'+elem.name+'-har.json'))
        elem.http_req_count= len(jsondata["log"]["entries"])

driver.quit();
server.stop();



# driver.close();
table= PrettyTable(['Website Name',"Request Code","HTTP Req Made"])
for i in data[:SIZE]:
    table.add_row([i.name,i.reqcode,i.http_req_count])
print(table)

