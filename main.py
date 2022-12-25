import requests
import re
from bs4 import BeautifulSoup
import os

def input_search_str():
    # searchStr = input('Enter your input:')
    searchStr = 'dua lipa'
    searchStr = searchStr.replace(' ', '+')
    return searchStr

def search_YT(searchQueryStr, mySearchStr):
    r = requests.get(searchQueryStr)
    # with open(f"{mySearchStr}.html", "w") as text_file:
    #     text_file.write(r.text)
    return (r.text)

def find_IDS(myText: str):
    return re.findall("webCommandMetadata\"\:{\"url\"\:\"(\/watch\?v=[^\"]+)", myText) 

def IDS_to_urls(videoIDS):
    videoURLS = []
    for url in videoIDS:
        url = 'https://www.youtube.com' + url
        videoURLS.append(url)
    return videoURLS

## main ##
numVideosWanted = 10

searchStr = input_search_str()
searchQueryStr = 'https://www.youtube.com/' + 'results?search_query=' + searchStr
print(searchQueryStr + '\n')

text = search_YT(searchQueryStr, searchStr)
videoIDS = (find_IDS(text))[:numVideosWanted]
videoURLS = IDS_to_urls(videoIDS)

print(videoURLS)
