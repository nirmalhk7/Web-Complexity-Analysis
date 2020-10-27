# # Characterizing Webpage Complexity and Its Impact

# onContentLoad- time taken to start rendering content
# onLoad- time taken to completely render all components on page
# number of objects loaded
# number of servers contacted

import csv
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
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
# os.system("rm -rf har_data/*")


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
options.add_argument('headless')
options.add_argument('ignore-certificate-errors')
options.add_argument("--proxy-server={}".format(proxy.proxy))
driver = webdriver.Chrome(chrome_options=options)

random.shuffle(data)

SIZE = 3
i=-1
valid200=0

while True:
    i+=1
    elem= data[i]
    print("Testing for",elem.name)
    try:
        elem.reqcode= requests.get("https://www."+elem.name).status_code
    except:
        elem.reqcode="N/A"
        continue
    if(200<=elem.reqcode<300):
        if(valid200>=SIZE):
            break;
        valid200+=1
        print("Opening ",elem.name)
        proxy.new_har(elem.name)
        driver.get('https://www.'+elem.name)
        driver.implicitly_wait(5)
        with open('har_data/'+elem.name+'-har.json','w') as har_file:
            json.dump(proxy.har,har_file)
        
        jsondata= json.load(open('har_data/'+elem.name+'-har.json'))

        request_arr=jsondata["log"]["entries"]
        for req in request_arr:
            elem.req_count["GET"]+=int(req["request"]["method"]=="GET")
            elem.req_count["POST"]+=int(req["request"]["method"]=="POST")
            # elem.req_count["PUT"]+=int(req["request"]["method"]=="PUT")
            # elem.req_count["DELETE"]+=int(req["request"]["method"]=="DELETE")
        
            

driver.quit();
server.stop();



# driver.close();

csv_rows=[]
csv_head=['Website Name',"Request Code","GET Req Count","POST Req Count"]
table= PrettyTable(csv_head)
for i in data[:SIZE]:
    details=[i.name,i.reqcode,i.req_count["GET"],i.req_count["POST"]]
    table.add_row(details)
    csv_rows.append(details)
print(table)

with open('./output.csv', 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(csv_head)  
        
    # writing the data rows  
    csvwriter.writerows(csv_rows)