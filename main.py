#!/usr/bin/python

from apiclient.discovery import build
from langdetect import detect

DEVELOPER_KEY = "DEVELOPER_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search():
    f = open('result', 'w+')
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q="",
        type="channel",
        regionCode="UA",
        relevanceLanguage="uk",
        part="id,snippet",
        maxResults=50,
    ).execute()
    
    search_channels = {}
    search_channels_str = ''
    
    for search_result in search_response.get("items", []):
        if ( len(search_result["snippet"]["title"]) > 0 and detect(search_result["snippet"]["title"]) == 'uk' ) or ( len(search_result["snippet"]["description"]) > 0 and detect(search_result["snippet"]["description"]) == 'uk' ):
            search_channels[search_result["id"]["channelId"]] = search_result["snippet"]["title"]
    
    print(str(search_response["pageInfo"]["totalResults"])+" "+str(search_response["pageInfo"]["resultsPerPage"]))
    
    while "nextPageToken" in search_response:
        search_response = youtube.search().list(
            q="",
            type="channel",
            regionCode="UA",
            relevanceLanguage="uk",
            part="id,snippet",
            maxResults=50,
            pageToken = search_response["nextPageToken"],
        ).execute()
        for search_result in search_response.get("items", []):
            if ( len(search_result["snippet"]["title"]) > 0 and detect(search_result["snippet"]["title"]) == 'uk' ) or ( len(search_result["snippet"]["description"]) > 0 and detect(search_result["snippet"]["description"]) == 'uk' ):
                search_channels[search_result["id"]["channelId"]] = search_result["snippet"]["title"]
        print(str(search_response["pageInfo"]["totalResults"])+" "+str(search_response["pageInfo"]["resultsPerPage"]))
    
    for k, v in search_channels.items():
        search_channels_str = search_channels_str + str(v) + "\n"
    
    f.write(search_channels_str)
    f.close()

youtube_search()
