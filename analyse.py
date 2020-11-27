import json
from prettytable import PrettyTable
from subprocess import Popen, PIPE


with open("./output.json") as file:
    websites = json.load(file)
count=len(websites)

info = {
    "Unclassified but Available": 0,
    "Classified but Unavailable (Not 200)": 0,
    "Classified and Available": 0,
    "Unclassified and Unavailable (Not 200)": 0,
    "Repeated Websites":0,
    "Average Rank":0
}

webdetails={}
webcategory={}
mime_used={}
for site in websites:
    try:
        webdetails[site["name"]]+=1
    except:
        webdetails[site["name"]]=1
    try:
        webcategory[site["category"]]+=1
    except:
        webcategory[site["category"]]=1
    if(site["category"]=="Unclassified"):
        if(site["reqcode"]=="N/A" or len(site["reqdetails"])==0):
            info["Unclassified and Unavailable (Not 200)"]+=1
        else:
            info["Unclassified but Available"]+=1
    else:
        if(site["reqcode"]=="N/A" or len(site["reqdetails"])==0):
            info["Classified but Unavailable (Not 200)"]+=1
        else:
            info["Classified and Available"]+=1
    if(webdetails[site["name"]]>1):
        info["Repeated Websites"]+=1
    info["Average Rank"]+=site["rank"]
    # for request in site["reqdetails"]:


info["Average Rank"]//=count
print("\nCategory-wise splitup:")
for t in sorted(webcategory.keys()):
    print("{}: {}".format(t,webcategory[t]))

print("")
for t in info.keys():
    print("{} : {}".format(t,info[t]))



print("")
print("{} websites scanned\n".format(count))


# Analyse number of object requests made

# Analyse MIME types used.

# Total Bytes downloaded

# Number of distinct servers
# '{uri.netloc}'.format(uri=urlparse(x))

# Number of Non-Origin Services

# Contribution of Non-Origin Services (in number of objects, bytes and contribution to the load time)

# Content breakdown of Non-Origin Services

# Origin vs Non-Origin Domains

# Classifying Non-Origin domains
