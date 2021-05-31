''' Test YtPlaylistCreator class '''

from yt_playlist_creator import YTPlaylistCreator

playlist_creator = YTPlaylistCreator()

playlist_creator.load_data('spotify', 'data/My Spotify Playlist.csv')

playlist_creator.tracks

playlist_creator.query_youtube()

playlist_creator.generate_playlist_urls()

print(i)