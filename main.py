import requests
import re
from bs4 import BeautifulSoup
import os
import shutil
from yt_dlp import YoutubeDL
import ffmpeg
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}

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

def requestYoutubePages(vidURLs):
    """
    returns list of HTML text of pages in input list
    """
    textList = []
    for link in vidURLS:
        r = requests.get(url=link, headers=headers)
        textList.append(r.text)
    return textList

def get_video_titles(pageHTMLList):
    """
    captures video titles
    """
    titleList = []
    for text in pageHTMLList:
        title = re.findall("<meta name=\"title\" content=\"(.*?)\">", text)
        titleList.append(title[0])
    return titleList

def clean_file_names(fileNames: list):
    newList = []
    for fileName in fileNames:
        newFileName = fileName.replace('/', '-')
        newFileName = newFileName.replace('&amp;', '&')
        newFileName = newFileName.replace('\\', '')
        newFileName = newFileName.replace('&quot;', "\"")
        newList.append(newFileName)
    return newList

def make_audio_directory(title: str):
    try:
        os.mkdir(title)
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
        'outtmpl': 'Audio' + '/%(title)s.%(ext)s' # download location is in "Audio" folder we made
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
    
def mergeLists(list1, list2):
    """
    merges 2 lists into 1 list of tuples
    """
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list


## main ##
numVideosWanted = 2
prefAudioFormat = 'mp3'

# # makes link for search term
searchStr = input_search_str()
searchQueryStr = 'https://www.youtube.com/' + 'results?search_query=' + searchStr

# # gets urls of first n videos from search (w)
r = search_YT(searchQueryStr) 
text = r.text                   ## HTML FROM SEARCH PAGE
vidIDS = (find_IDS(text))
vidIDS = (remove_vids_w_timer(vidIDS))[:numVideosWanted]
vidURLS = IDS_to_urls(vidIDS)
# print(vidIDS)
# print(vidURLS)

# request youtube pages
textList = requestYoutubePages(vidURLS)

# gets video titles
vidTitles = (get_video_titles(textList))[:numVideosWanted]
vidTitles = clean_file_names(vidTitles)
# print(vidTitles)

# tuple vid ids and titles
myList = mergeLists(vidIDS, vidTitles)
# print(myList)

# # make transcript folder
make_audio_directory('Transcripts')

# # transcript section
for i in myList:
    transcript = YouTubeTranscriptApi.get_transcript(i[0])
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcripts(transcript, indent=2) # .format_transcript(transcript) turns the transcript into a JSON string.
    # Now we can write it out to a file.
    with open(os.path.join('./Transcripts', f'{i[1]}.json'), 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)
    # Now should have a new JSON file that you can easily read back into Python.

# # audio section
download_audio(vidURLS, prefAudioFormat) 
