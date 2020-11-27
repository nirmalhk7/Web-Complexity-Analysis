import csv
from Website import websiteDetails
import json
from urllib.parse import urlparse
from tldextract import extract
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from clean import cleanArr
import argparse
from prettytable import PrettyTable
from siteCategory import getCategory


def isNonOrigin(site,link):
    return extract(site).domain!=extract(link).domain

def parseNonOrigins():

    # print(isNonOrigin(x,'c.com'))
    data={}
    with open("dataset.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            data[row["name"]]=int(row["rank"])
    print("Dataset read")
    with open("output.json", "r") as jsonFile:
        website_data = json.load(jsonFile)
    print("Collected Data read")
    website_data=cleanArr(website_data)[0]
    non_origin_hash={}
    new_non_origin_hash={}
    totalCount=0
    for site in website_data:
        print("{}: Parsing Non-Origin Content".format(site['name']))
        for req in site['reqdetails']:
            if isNonOrigin(site['name'],req['reqUrl']):
                totalCount+=1
                try:
                    non_origin_hash[extract(req['reqUrl']).domain+'.'+extract(req['reqUrl']).suffix]+=1
                except:
                    non_origin_hash[extract(req['reqUrl']).domain+'.'+extract(req['reqUrl']).suffix]=1
    totalv=0
    print('Reformatting Non-Origin Content')
    for k, v in sorted(non_origin_hash.items(), key=lambda item: item[1],reverse=True):
        if(round(v/totalCount,2)!=0.0):
            with open("./nonorigin.json") as file:
                nonorigin = json.load(file)
            if k not in nonorigin:
                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                options.add_argument("ignore-certificate-errors")
                driver_category = webdriver.Chrome(options=options)
                category=getCategory('www.'+k,driver_category)
                driver_category.quit()
                print("{}: Categorized as {}".format(k,category))
                print("{}: Writing to file ....".format(k))
                try:
                    nonorigin[k]={"probability":round(v/totalCount,4),"rank":data[k],"category":category,'found_count':v}
                except:
                    nonorigin[k]={"probability":round(v/totalCount,4),"rank":"N/A","category":category,'found_count':v}
                with open("./nonorigin.json", "w") as jsonFile:
                    json.dump(nonorigin, jsonFile, indent=4)
        
    for x in new_non_origin_hash.keys():
        print("{}: {}".format(x,new_non_origin_hash[x]))

def analyseNonOrigins():
    with open("nonorigin.json", "r") as jsonFile:
        website_data = json.load(jsonFile)
    table_arr=[['Rank','Name','Fraction of Sites','Types']]
    for site in website_data.keys():
        try:
            table_arr.append([int(website_data[site]['rank']),site,website_data[site]['probability'],website_data[site]['category']])
        except Exception as e:
            continue
    table_arr[1:]=sorted(table_arr[1:],key=lambda x:x[2],reverse=True)
    table=PrettyTable(table_arr[0])
    for i in range(1,len(table_arr)):
        table.add_row(table_arr[i])
    print(table_arr)

def analyseNonOrigins_1():
    with open("output.json", "r") as jsonFile:
        website_data = json.load(jsonFile)
    totalCount=0
    for site in website_data:
        for req in site['reqdetails']:
            if isNonOrigin(site['name'],req['reqUrl']):
                totalCount+=1
    with open("nonorigin.json", "r") as jsonFile:
        no_data = json.load(jsonFile)
    no_data_arr=[['Rank','Name','Number of Sites','Types']]
    for no in no_data:
        no_data_arr.append([no_data[no]['rank'],no,int(no_data[no]['probability']*totalCount),no_data[no]['category']])
    print(no_data_arr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parse", help="Count of website to generate data for")
    args = parser.parse_args()
    if(not args.parse):
        args.parse='True'
    checkParse= args.parse.lower()=='true'
    if(checkParse):
        parseNonOrigins()
    # analyseNonOrigins()
    analyseNonOrigins_1()
    pass