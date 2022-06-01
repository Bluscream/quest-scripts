from re import match
from subprocess import check_output
from logging import *
basicConfig(
    level=DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding='utf-8',
    handlers=[
        FileHandler(f'{__file__}.log'),
        StreamHandler()
    ]
)
from pathlib import PurePosixPath
remote_songfolder = PurePosixPath("/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/")

def ls_by_line(path):
    return check_output(["adb","shell",f"ls \"{path}\""]).decode().splitlines()
def rm(path):
    return check_output(["adb","shell",f"rm -rf \"{path}\""]).decode().splitlines()

def is_song_hashed(song_dir_name):
    return True if match(r'[0-9a-f]{40}', song_dir_name) else False
print(remote_songfolder)
uploaded_songs = ls_by_line(remote_songfolder)
for song in uploaded_songs:
    if not is_song_hashed(song):
        song = remote_songfolder / song
        print(f"Removing {song}")
        rm(song)