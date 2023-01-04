import requests
import re
from bs4 import BeautifulSoup
import os
from yt_dlp import YoutubeDL
import ffmpeg
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

headers = {'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2'}

def input_search_str():
    """
    takes input from user
    creates url ready string for youtube link
    """
    # searchStr = input('Enter your input:')
    searchStr = 'ted talk'
    # searchStr = 'dua lipa'
    searchStr = searchStr.replace(' ', '+')
    return searchStr

def search_YT(url):
    """
    sends request to youtube with search string
    """
    r = requests.get(url=url, headers=headers)
    return r

def find_IDS(myText: str):
    """
    capture youtube video ids from search page
    """
    return re.findall("webCommandMetadata\"\:{\"url\"\:\"\/watch\?v=([^\"]+)", myText) 

def remove_vids_w_timer(vidIDS):
    newList = []
    for ids in vidIDS:
        if 't=' not in ids:
            newList.append(ids)
    return newList

def IDS_to_urls(videoIDS):
    """
    converts youtube ids to links
    """
    videoURLS = []
    for id in videoIDS:
        url = 'https://www.youtube.com/watch?v=' + id
        videoURLS.append(url)
    return videoURLS

def get_video_titles(myText: str):
    """
    captures video titles
    """
    titleList = re.findall("\"title\":{\"runs\":\[{\"text\":\"(.*?)accessibility", myText)
    newTitleList = []
    for title in titleList:
        title = title[:-5]
        newTitleList.append(title)
    return newTitleList

def clean_file_names(fileNames: list):
    newList = []
    for fileName in fileNames:
        newFileName = fileName.replace('/', '-')
        newFileName = newFileName.replace('&amp;', '&')
        newList.append(newFileName)
    return newList

def make_audio_directory():
    try:
        os.mkdir('Audio')
    except OSError as error:
        print(error)

def download_audio(link, prefFormat):
    """
    downloads youtube video audio with yt-dlp
    """
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': prefFormat,  # converts our file to mp3 with ffmpeg module
        }],
        'outtmpl': 'Audio/%(title)s.%(ext)s' # download location is in "Audio" folder we made
    }
    with YoutubeDL(ydl_opts) as ydl:
        errorCode = ydl.download(link)
    

def get_transcript(vidID):
    """
    gets youtube transcripts into JSON file
    """
    # assigning srt variable with the list
    # of dictionaries obtained by the get_transcript() function
    try:
        srt = YouTubeTranscriptApi.get_transcript(vidID)
        # prints the result
        return srt
    except Exception as e:
        print(e)
    

## main ##
numVideosWanted = 4
prefAudioFormat = 'mp3'

# # makes link for seasch term
searchStr = input_search_str()
searchQueryStr = 'https://www.youtube.com/' + 'results?search_query=' + searchStr

# # gets urls of first n videos from search (w)
r = search_YT(searchQueryStr)
text = r.text
vidIDS = (find_IDS(text))
vidIDS = (remove_vids_w_timer(vidIDS))[:numVideosWanted]
vidURLS = IDS_to_urls(vidIDS)
# print(vidIDS)
# print(vidURLS)

# gets video titles
vidTitles = (get_video_titles(text))[:numVideosWanted]
vidTitles = clean_file_names(vidTitles)
# print(vidTitles)

# tuple vid ids and titles
myList = []
[myList.append((ids, titles)) for ids in vidURLS for titles in vidTitles]
print(myList)

# # transcript section
# for i in vidIDS:
#     transcript = YouTubeTranscriptApi.get_transcript(i)
#     formatter = JSONFormatter()
#     json_formatted = formatter.format_transcripts(transcript, indent=2) # .format_transcript(transcript) turns the transcript into a JSON string.
#     # Now we can write it out to a file.
#     with open(f'{i}.json', 'w', encoding='utf-8') as json_file:
#         json_file.write(json_formatted)
#     # Now should have a new JSON file that you can easily read back into Python.


# # audio part (w)
# make_audio_directory()
# download_audio(vidURLS, prefAudioFormat) 
