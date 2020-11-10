import json
import statistics

def cleanArr(websites):
    new_websites = []
    rank_arr = []
    mime_list = {}
    category = {}
    for index, site in enumerate(websites):
        if (
            site["reqcode"] == "N/A"
            or len(site["reqdetails"]) == 0
            or site["category"] == "Unclassified"
        ):
            continue
        else:
            try:
                category[site["category"]] += 1
            except:
                category[site["category"]] = 1
            detail_arr = []
            rank_arr.append((site["rank"], index))
            for detail in site["reqdetails"]:
                detail["mimeType"] = detail["mimeType"].split(";")[0]
                if detail["mimeType"]:
                    c1 = detail["mimeType"].split("/")[0]
                    try:
                        c2 = detail["mimeType"].split("/")[1]
                    except Exception as e:
                        c2 = ""
                    c1, c2 = c1.lower(), c2.lower()
                    if c1 == "image":
                        detail["mimeType"] = "image"
                    elif (
                        c1 == "javascript" or c2 == "javascript" or c2 == "x-javascript"
                    ):
                        detail["mimeType"] = "javascript"
                    elif c2 == "json":
                        detail["mimeType"] = "json"
                    elif c1 == "video":
                        detail["mimeType"] = "video"
                    elif c1 == "font" or c1 == "x-font":
                        detail["mimeType"] = "font"
                    elif c1 == "audio":
                        detail["mimeType"] = "audio"
                    elif c2 == "css" or c1 == "css":
                        detail["mimeType"] = "css"
                    else:
                        continue
                    try:
                        mime_list[detail["mimeType"]] += 1
                    except:
                        mime_list[detail["mimeType"]] = 1
                    detail_arr.append(detail)
            site["reqdetails"] = detail_arr
        new_websites.append(site)
    return new_websites, mime_list, category, rank_arr


if __name__ == "__main__":
    with open("./output.json") as file:
        websites = json.load(file)
    cleanArr(websites)