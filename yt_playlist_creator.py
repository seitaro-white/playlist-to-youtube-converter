''' Playlist creator class '''

import time

import xml.etree.ElementTree as ET

import pandas as pd
from tqdm import tqdm
from youtubesearchpython import VideosSearch


class YTPlaylistCreator():

    def __init__(self):
        ''' Initialise class '''
        self.tracks = []
        self.query_results = []
        self.yt_playlist_urlheader = 'http://www.youtube.com/watch_videos?video_ids='


    def load_data(self, source_format, file):
        ''' Factory class to load data into tracks '''

        if source_format == 'itunes' and file[-3:] == 'xml':
            self.tracks = self._parse_itunes_pl(file)

        elif source_format == 'spotify' and file[-3:] == 'csv':
            self.tracks = self._parse_spotify_pl(file)

        else:
            raise ValueError('Invalid playlist file format!')

    @staticmethod
    def _parse_itunes_pl(file):
        ''' Parse XML playlist export from iTunes '''
        
        root = ET.parse(file).getroot()

        tracks = []
        for track in root.findall('dict/dict/dict'):
            track_name = track.findall('string')[0].text
            track_artist = track.findall('string')[1].text
            track_album = track.findall('string')[4].text

            tracks.append({
                'track_name': track_name,
                'track_artist': track_artist,
                'track_album': track_album})

        return tracks
        
    @staticmethod
    def _parse_spotify_pl(file):
        ''' Parse CSV playlist export from Spotify '''

        df = pd.read_csv(file, encoding='utf-8-sig')
        tracks = df[['Track name', ' Artist name', ' Album']].to_dict(orient='records')

        return tracks


    def query_youtube(self):
        ''' Search all tracks in youtube and get search results back '''

        for i in tqdm(self.tracks):
            query = f'{i[" Artist name"]} {i["Track name"]} {i[" Album"]}'
            
            videosSearch = VideosSearch(query, limit = 1)
            result = videosSearch.result()['result'][0]

            self.query_results.append({
                'query': query,
                'title': result['title'],
                'channel': result['channel']['name'],
                'video_id': result['id']})

            time.sleep(2)

    
    def generate_playlist_urls(self):
        ''' Generate youtuve playlists from query results '''
        
        playlist_urls = []
        video_id_chunks = [self.query_results[i:i + 50] 
                           for i in range(0, len(self.query_results), 50)] 
        
        for i in video_id_chunks:
            video_id_string = ','.join([i['video_id'] for i in self.query_results])
            url = self.yt_playlist_urlheader + video_id_string
            playlist_urls.append(url)

        return playlist_urls


