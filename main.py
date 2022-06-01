import datetime

from ytmusicapi import YTMusic
from pprint import pformat, pprint
from typing import List
from datetime import datetime
from json import dumps

ytm = YTMusic('headers_auth.json')
# ytm.setup(filepath='headers_auth.json', headers_raw="""""")

_songs = []

def get_song_ids(songs: List[dict]):
    global _songs
    ret = []
    for song in songs:
        # if hasattr(song, "id"): _songs.append(song["id"])
        if "videoId" in song:
            ret.append(song["videoId"])
        else: print(f"ERROR - Song has no videoId: {dumps(song)}")
    print(f"Got {len(ret)} song ids from {len(songs)} songs")
    _songs += ret
    return ret

def get_playlist_description(name):
    return f"Migrated with ytmusicapi in python at {datetime.now()}"

def create_playlist(name, video_ids = None):
    description = get_playlist_description(name)
    print(f"Creating playlist with name={name} description={description}")
    return ytm.create_playlist(name, description, "PUBLIC", video_ids)

def recreate_playlist(playlistId: str, name):
    print(f"Deleting playlist {playlistId}")
    ytm.delete_playlist(playlistId)
    return create_playlist(name)

def create_or_update_playlist(name: str, songs: List[str]):
    playlists = ytm.get_library_playlists(limit=150)
    print(f"Found {len(playlists)} playlists in current library")
    duplicates = []
    for playlist in playlists:
        if playlist["title"] == name: duplicates.append(playlist["playlistId"])
    print(f"Found {len(duplicates)} playlists with name \"{name}\"")
    for duplicate in duplicates[1:]:
        print(f"Deleting duplicate playlist {duplicate}")
        ytm.delete_playlist(duplicate)
    if len(duplicates) < 1:
        print(f"Playlist \"{name}\" does not exist yet, creating...")
        duplicates.append(create_playlist(name))
    else:
        duplicates[0] = recreate_playlist(duplicates[0], name)
    # pl = ytm.get_playlist(duplicates[0], 5000)
    # ytm.remove_playlist_items(duplicates[0], pl["tracks"])
    ytm.add_playlist_items(duplicates[0], songs)

create_or_update_playlist("Library Songs", get_song_ids(ytm.get_library_songs(5000)))
create_or_update_playlist("Liked Songs", get_song_ids(ytm.get_liked_songs(5000)["tracks"]))

def chunks(l,n): return [l[i:i + n] for i in range(0, len(l), n)]
_songs_ = len(_songs)
_songs = list(set(_songs))
print(f"{_songs_} total songs ({_songs_ - len(_songs)} duplicates)")
i = 0
with open("songs.txt", "w") as f:
    for song in _songs:
        i += 1
        if i % 100 == 0: f.write(f"# {i} - {i+100}\n")
        f.write(f"https://music.youtube.com/watch?v={song}\n")

exit()