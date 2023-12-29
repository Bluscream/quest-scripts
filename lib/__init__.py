from ytmusicapi import YTMusic
from datetime import datetime
from json import dumps
from urllib.parse import urlparse, parse_qs


def get_song_ids(songs: list[dict]):
    ret = []
    for song in songs:
        # if hasattr(song, "id"): _songs.append(song["id"])
        if "videoId" in song:
            ret.append(song["videoId"])
        else: print(f"ERROR - Song has no videoId: {dumps(song)}")
    print(f"Got {len(ret)} song ids from {len(songs)} songs")
    return ret

def get_playlist_description(name):
    return f"Migrated with ytmusicapi in python at {datetime.now()}"

def create_playlist(ytm: YTMusic, name, video_ids = None):
    description = get_playlist_description(name)
    print(f"Creating playlist with name={name} description={description}")
    return ytm.create_playlist(name, description, "PUBLIC", video_ids)

def recreate_playlist(ytm: YTMusic, playlistId: str, name, video_ids: list[str] = None):
    print(f"Deleting playlist {playlistId}")
    ytm.delete_playlist(playlistId)
    return create_playlist(ytm, name, video_ids)

def create_or_update_playlist(ytm: YTMusic, name: str, videoIds: list[str]):
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
        duplicates[0] = recreate_playlist(ytm, duplicates[0], name, videoIds)
    # pl = ytm.get_playlist(duplicates[0], 5000)
    # ytm.remove_playlist_items(duplicates[0], pl["tracks"])
    ytm.add_playlist_items(duplicates[0], videoIds)

def s(l: dict): return f"'{l['title']}' ({l['id']}) [{len(l['tracks'])}]"
def get_playlist(ytm: YTMusic, playlist_id):
    if "music.youtube.com/playlist" in playlist_id:
        parsed_url = urlparse(playlist_id)
        playlist_id = parse_qs(parsed_url.query)['list'][0]
    playlist = ytm.get_playlist(playlist_id)
    if 'tracks' not in playlist:
        print(f"Playlist {s(playlist)} does not have any tracks.")
        return 
    for i, track in enumerate(playlist["tracks"]):
        if not "videoId" in track: print(f"videoId not found in #{i} {track['title']}")
        if not "setVideoId" in track: print(f"setVideoId not found in #{i} {track['title']}")
    return playlist
def clear_playlist(ytm: YTMusic, playlist):
    print(f"Removing tracks from {s(playlist)}...")
    ytm.remove_playlist_items(playlist["id"], playlist['tracks'])
def reverse_playlist(ytm: YTMusic, playlist):
    reversed_ids = [t["videoId"] for t in playlist['tracks']]
    reversed_ids.reverse()
    clear_playlist(playlist)
    ytm.add_playlist_items(playlistId=playlist["id"], videoIds=reversed_ids)
    new_description = f'{playlist["description"] or ""}\nReversed using ytmusicapi at {datetime.now()}'
    print(f"Updating playlist description to:\n{new_description}")
    ytm.edit_playlist(playlist["id"], description=new_description)
    print(f"Playlist {s(playlist)} has been reversed!")