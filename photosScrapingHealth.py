from medinify.scrapers import WebMDScraper, DrugRatingzScraper, DrugsScraper, EverydayHealthScraper
import pandas as pd
import json
from bs4 import BeautifulSoup
import urllib
import requests
from PIL import Image
import urllib.request
from io import BytesIO

def get_image(url, name):
    query_url = ""
    try :
        query_url = urllib.request.urlopen(url)
    
    except Exception as e:
        print("Could not get image at " + url)
        print(e)
        return

    file = BytesIO(query_url.read())
    im = Image.open(file)
    width, height = im.size
    fileFormat = im.format
    return {"namePhoto": name, "url" : url, "width" : width, "height": height, "format" : fileFormat}

input_list = ["yikjnlml" , "adderall"]

correct_list =[]

aggregatePhotos = []

for i in range(len(input_list)):
    
    url = "https://www.everydayhealth.com/drugs/"+input_list[i]
    r = requests.get(url)
    
    if r.status_code != 200:
        print("Could not connect to " + url)
        print("Response : " + str(r.status_code))
        continue

    correct_list.append(input_list[i])
    bs = BeautifulSoup(requests.get(url).text, 'html.parser')
    
    
    json_object = {"name": input_list[i] }
    photos = []
    b2 = bs.findAll("div", {"class" : "drug-image"})
    for b4 in b2 :
        if b4.findChildren("img")[0].attrs["src"] != "" :
            src = b4.findChildren("img")[0].attrs["src"]
            photos.append(get_image("https:" + src,input_list[i]))
        elif b4.findChildren("img")[0].attrs["data-src"] != "" :
            src = b4.findChildren("img")[0].attrs["data-src"]
            photos.append(get_image("https:" + src,input_list[i]))
    json_object["photos"] = photos
    aggregatePhotos.append(json_object)

json_aggregatePhotos = {"website" : "everydayhealth.com"}

json_aggregatePhotos["namesItems"] = correct_list

json_aggregatePhotos["photosAggregation"] =  aggregatePhotos

with open("photosResult.json","w") as f:
    obj = json.dumps(json_aggregatePhotos, indent = 4 )
    f.write(obj)

