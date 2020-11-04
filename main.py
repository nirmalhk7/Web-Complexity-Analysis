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
from siteCategory import getCategory
import time

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--count", help="Count of website to generate data for")

args = parser.parse_args()
# https://dzone.com/articles/performance-capture-i-export-har-using-selenium-an
print("Arguments passed", args)
data = []


"""Delete previous screenshots and har_data"""
os.system("rm -rf screenshots/*")
# if(args.regenerate):
# os.system("rm -rf har_data/*")


"""Read CSV file"""
with open("dataset.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        data.append(websiteDetails(row["name"], int(row["rank"])))
        line_count += 1


"""Start browsermob-proxy server"""
# https://stackoverflow.com/questions/48201944/how-to-use-browsermob-with-python-selenium
server_port = 8090
server = Server(
    "./browsermob-proxy-2.1.4/bin/browsermob-proxy", options={"port": server_port}
)
server.start()
proxy = server.create_proxy()
print("browsermob-proxy active on {}".format(server_port))


"""Set options for Chrome browser"""
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("ignore-certificate-errors")

driver_category = webdriver.Chrome(options=options)
options.add_argument("--proxy-server={}".format(proxy.proxy))
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(60)
random.shuffle(data)
print("Data randomised")

json_arr = []
csv_head = [
    "Rank",
    "Website Name",
    "Category",
    "Request Code",
]
table = PrettyTable(csv_head)


i = 0
SIZE = int(args.count or 5)

while SIZE > 0:
    i += 1
    elem = data[i]
    print("Testing for", elem.name)
    try:
        elem.reqcode = requests.get("https://www." + elem.name).status_code
    except:
        print("Failed for https://www." + elem.name, elem.reqcode)
        elem.reqcode = elem.category = "N/A"
        elem.req_count["POST"] = elem.req_count["GET"] = 0
    elem.category = "Unclassified"
    if elem.reqcode != "N/A":
        if 200 <= elem.reqcode < 300:
            print(SIZE, "Opening ", elem.name, elem.reqcode)
            proxy.new_har(elem.name)
            try:
                driver.get("https://www." + elem.name)
                driver.implicitly_wait(5)
                with open("har_data/" + elem.name + "-har.json", "w") as har_file:
                    json.dump(proxy.har, har_file)
                print("Dumped HAR file",elem.name)
                jsondata = json.load(open("har_data/" + elem.name + "-har.json"))
                elem.category = getCategory("www." + elem.name, driver_category)
                request_arr = jsondata["log"]["entries"]
                for req in request_arr:
                    elem.requestDetails.append(
                        {
                            "time": req["time"],
                            "mimeType": req["response"]["content"]["mimeType"],
                            "responseSize": req["response"]["bodySize"],
                            "reqUrl": req["request"]["url"],
                            "method": req["request"]["method"],
                            "started": req["startedDateTime"]
                        }
                    )
                SIZE -= 1
                print("Parsed Req-Res details",elem.name)
            except Exception as e:
                print(e)
    # details =
    with open("output.json", "r") as jsonFile:
        output_data = json.load(jsonFile)
    output_data.append(
        {
            "rank": elem.rank,
            "name": elem.name,
            "category": elem.category,
            "reqcode": elem.reqcode,
            "reqdetails": elem.requestDetails,
        }
    )
    with open("./output.json", "w") as jsonFile:
        json.dump(output_data, jsonFile)
    table.add_row([elem.rank, elem.name, elem.category, elem.reqcode])

driver.quit()
server.stop()

print(table)

print("")
print(len(json.load(open("./output.json"))),"websites already pinged.")

# with open('./output.csv', 'a') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerows(csv_rows)