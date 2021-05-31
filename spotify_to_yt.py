''' Load Spotify Data and search Youtube API '''
# %%
# Imports
import time

import xml.etree.ElementTree as ET

import pandas as pd
from tqdm import tqdm
from youtubesearchpython import VideosSearch

# %%
# Load Playlist Data

playlist = pd.read_csv('data\My Spotify Playlist.csv', encoding='utf-8-sig')

tracks = playlist[['Track name', ' Artist name', ' Album']].to_dict(orient='records')

# %%
query_results = []

for i in tqdm(tracks):
    query = f'{i[" Artist name"]} {i["Track name"]} {i[" Album"]}'
    
    videosSearch = VideosSearch(query, limit = 1)
    result = videosSearch.result()['result'][0]

    query_results.append({
        'query': query,
        'title': result['title'],
        'channel': result['channel']['name'],
        'video_id': result['id']})

    time.sleep(2)

# %%
playlist_url = 'http://www.youtube.com/watch_videos?video_ids='

for i in query_results:
    playlist_url += i['video_id']
    playlist_url += ','

playlist_url = playlist_url[:-1]
# %%
