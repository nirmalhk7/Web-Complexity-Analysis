import json
import os
from Website import websiteDetails
from siteCategory import getCategory
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from prettytable import PrettyTable
import csv
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--count", help="Count of website to generate data for")
args = parser.parse_args()
defcount= int(args.count)-1 or 1000000000000
print("Arguments passed", args)

data = {}
with open("dataset.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data[row["name"]]=row["rank"]

site_names = {}
with open("./output.json") as file:
    websites = json.load(file)
for site in websites:
    site_names[site["name"]] = True


table = PrettyTable(
    [
        "Rank",
        "Website Name",
        "Category",
        "Request Code",
    ]
)



has_har = os.listdir("har_data")

counter=0
for s in has_har:
    name = s.split("-har.json")[0]
    if name not in site_names.keys():
        counter+=int(name not in site_names.keys())
inp_count=0
for s in has_har:
    name = s.split("-har.json")[0]
    if inp_count>defcount:
        break
    if name not in site_names.keys():
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("ignore-certificate-errors")
        driver_category = webdriver.Chrome(options=options)
        print("{}: Processing. Websites Remaining: {}".format(name,counter))
        site = websiteDetails(
            name,data[name]
        )
        site.name = name
        site.reqcode = 200
        print("{}: Fetching Category".format(name))
        try:
            site.category = getCategory(
                "www." + name,driver_category
            )
        except Exception as e:
            site.category = "Unclassified"
            print("{}: {}".format(name, e))
        print("{}: Category recieved ({}). Now parsing the HAR file".format(name,site.category))
        with open('har_data/'+s, "r") as file:
            site_har = json.load(file)
        site_har = site_har["log"]["entries"]
        for req in site_har:
            site.requestDetails.append(
                {
                    "time": req["time"],
                    "mimeType": req["response"]["content"]["mimeType"],
                    "responseSize": req["response"]["bodySize"],
                    "reqUrl": req["request"]["url"],
                    "method": req["request"]["method"],
                    "started": req["startedDateTime"],
                }
            )
        
        websites.append(
            {
                "rank": site.rank,
                "name": site.name,
                "category": site.category,
                "reqcode": site.reqcode,
                "reqdetails": site.requestDetails,
            }
        )
        print("{}: Dumping output. Please dont force shutdown now ...".format(name))
        with open("./output.json", "w") as jsonFile:
            json.dump(websites, jsonFile, indent=4)
        print("{}: Data dumped.".format(name))
        table.add_row([site.rank, site.name, site.category, site.reqcode])
        driver_category.quit()
        counter-=1
        inp_count+=1

print(table)