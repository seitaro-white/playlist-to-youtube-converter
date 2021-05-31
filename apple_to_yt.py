''' Load Apple Data and search Youtube API '''
# %%
# Imports
import time

import xml.etree.ElementTree as ET

from tqdm import tqdm
from youtubesearchpython import VideosSearch

# %% Load playlist data
root = ET.parse('data\Edgy Alternative Stuff.xml').getroot()

tracks = []
for track in root.findall('dict/dict/dict'):
    track_name = track.findall('string')[0].text
    track_artist = track.findall('string')[1].text
    track_album = track.findall('string')[4].text

    tracks.append({
        'track_name': track_name,
        'track_artist': track_artist,
        'track_album': track_album})

# %%
# Query youtube search

query_results = []
for i in tqdm(tracks):
    query = f'{i["track_artist"]} {i["track_name"]} {i["track_album"]}'
    
    videosSearch = VideosSearch(query, limit = 1)
    result = videosSearch.result()['result'][0]

    query_results.append({
        'query': query,
        'title': result['title'],
        'channel': result['channel']['name'],
        'video_id': result['id']})

    time.sleep(2)


# %%
# Create Playlist link
playlist_url = 'http://www.youtube.com/watch_videos?video_ids='

for i in query_results:
    playlist_url += i['video_id']
    playlist_url += ','

playlist_url = playlist_url[:-1]

# %%
