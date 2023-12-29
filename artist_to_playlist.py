from ytmusicapi import YTMusic, setup
from lib import create_or_update_playlist, get_song_ids

# Initialize YTMusic
# setup(filepath="headers_auth.json", headers_raw=open("headers_raw.txt").read())
ytm = YTMusic('headers_auth.json') 

# Define the artist name
artist_name = input('Enter the artist name: ')
playlist_name = 'Top Songs of ' + artist_name

# Search for the artist
search_results = ytm.search(artist_name, filter='artists')

# Get the artist's information
artist_info = ytm.get_artist(search_results[0]['browseId'])

# Get the artist's top songs
top_songs = artist_info['songs']['results']

# Create a new playlist
create_or_update_playlist(ytm, playlist_name, get_song_ids(top_songs))
