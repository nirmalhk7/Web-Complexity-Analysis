import json
from prettytable import PrettyTable

with open("./output.json") as file:
    websites = json.load(file)
count=len(websites)
print("{} websites scanned".format(count))
info = {
    "Unclassified but Available": 0,
    "Classified but Unavailable (Not 200)": 0,
    "Classified and Available": 0,
    "Unclassified and Unavailable (Not 200)": 0,
    "Repeated Websites":0,
    "Average Rank":0
}
webdetails={}
for site in websites:
    try:
        webdetails[site["name"]]+=1
    except:
        webdetails[site["name"]]=1
    if(site["category"]=="Unclassified"):
        if(site["reqcode"]=="N/A"):
            info["Unclassified and Unavailable (Not 200)"]+=1
        else:
            info["Unclassified but Available"]+=1
    else:
        if(site["reqcode"]=="N/A"):
            info["Classified but Unavailable (Not 200)"]+=1
        else:
            info["Classified and Available"]+=1
    if(webdetails[site["name"]]>1):
        info["Repeated Websites"]+=1
    info["Average Rank"]+=site["rank"]

info["Average Rank"]//=count
for t in info.keys():
    print(t+" : {}".format(info[t]))
