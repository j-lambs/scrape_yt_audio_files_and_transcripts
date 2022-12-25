import requests
import re
from bs4 import BeautifulSoup
import os
from yt_dlp import YoutubeDL
import ffmpeg

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

def make_audio_directory():
    try:
        os.mkdir('./Audio')
    except OSError as error:
        print(error)

def downloadAudio(link, prefFormat):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': prefFormat,  # converts our file to mp3 with ffmpeg module
        }],
        'outtmpl': './Audio/%(title)s.%(ext)s' # download location is in "Audio" folder we made
    }
    with YoutubeDL(ydl_opts) as ydl:
        errorCode = ydl.download(link)
    
## main ##
numVideosWanted = 10
prefAudioFormat = 'mp3'

searchStr = input_search_str()
searchQueryStr = 'https://www.youtube.com/' + 'results?search_query=' + searchStr
print(searchQueryStr + '\n')

text = search_YT(searchQueryStr, searchStr)
videoIDS = (find_IDS(text))[:numVideosWanted]
videoURLS = IDS_to_urls(videoIDS)

# print(videoURLS)

downloadAudio(videoURLS, prefAudioFormat)
