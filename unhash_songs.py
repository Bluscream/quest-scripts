import hashlib
from re import match
from subprocess import check_output
from time import sleep
from logging import *
from json import load
basicConfig(
    level=DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding='utf-8',
    handlers=[
        FileHandler(f'{__file__}.log'),
        StreamHandler()
    ]
)
from pathlib import Path
local_songfolder = Path(r"G:\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels")

import os
from fnmatch import filter
def get_info_dat(song_dir: str): return song_dir + "/" + filter(os.listdir(song_dir), '[Ii][Nn][Ff][Oo].[Dd][Aa][Tt]')[0]
def get_song_info(song_info_file: str):
    with open(str(song_info_file), 'rb') as info_dat: return load(info_dat)
def is_song_hashed(song_dir_name): return True if match(r'[0-9a-f]{40}', song_dir_name) else False

def get_song_filename(song_dir):
    song_info = get_song_info(song_dir)
    return f'[BSD] {song_info["_songName"]} - {song_info["_songAuthorName"]}'

for song in local_songfolder.iterdir():
    if is_song_hashed(song.name):
        try:
            unhashed_name = get_song_filename(str(song))
            info(f"Unhashing {song.name} to {unhashed_name}")
            os.rename(song, str(song.parent) + "/" + unhashed_name)
        except PermissionError as e: print(e)