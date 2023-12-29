from ytmusicapi import YTMusic
from pprint import pformat, pprint
from json import dumps
from lib import create_or_update_playlist, get_song_ids

ytm = YTMusic('headers_auth.json')
# ytm.setup(filepath='headers_auth.json', headers_raw="""""")


# with open("access_token.txt", "r") as f:
#     from pyyoutube import Api as Youtube
#     token = f.read()
#     yt = Youtube(access_token=token)
#     # my_playlists = yt.get_playlists(mine=True)
#     my_channel = yt.get_channel_info(mine=True)
#     pprint(my_channel.items[0])

# playlist = get_playlist("https://music.youtube.com/playlist?list=PLZcTzTcUhr8U5f3OvaFczQR2y6QwxOuCs&feature=share")
# reverse_playlist(playlist)
library_songs = ytm.get_library_songs(7500)
print(f"Got {len(library_songs)} songs from library")
create_or_update_playlist(ytm, "Library Songs", get_song_ids(library_songs))
liked_songs = ytm.get_liked_songs(7500)["tracks"]
print(f"Got {len(liked_songs)} liked songs")
create_or_update_playlist(ytm, "Liked Songs", get_song_ids(liked_songs))
# create_or_update_playlist("Special Songs", ["AK-O9QRtOIk"])

# def chunks(l,n): return [l[i:i + n] for i in range(0, len(l), n)]
# _songs_ = len(_songs)
# _songs = list(set(_songs))
# print(f"{_songs_} total songs ({_songs_ - len(_songs)} duplicates)")
# i = 0
# with open("songs.txt", "w") as f:
#     for song in _songs:
#         i += 1
#         if i % 100 == 0: f.write(f"# {i} - {i+100}\n")
#         f.write(f"https://music.youtube.com/watch?v={song}\n")

exit()