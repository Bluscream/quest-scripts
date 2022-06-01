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

def is_song_hashed(song_dir_name):
    return True if match(r'[0-9a-f]{40}', song_dir_name) else False

import os
from fnmatch import filter
def get_info_dat(song_dir: str):
    return song_dir + "/" + filter(os.listdir(song_dir), '[Ii][Nn][Ff][Oo].[Dd][Aa][Tt]')[0]

def get_song_info(song_info_file: str):
    with open(str(song_info_file), 'rb') as info_dat:
        return load(info_dat)

def get_song_hash(path: str):
    song_info_file = get_info_dat(path)
    print(song_info_file)
    song_info = get_song_info(song_info_file)
    print(song_info)
    hash_obj = hashlib.sha1(open(song_info_file, 'rb').read())
    difficulty_files = []
    for beatmapset in song_info['_difficultyBeatmapSets']:
        for beatmap in beatmapset["_difficultyBeatmaps"]:
            difficulty_files.append(path + "/" + beatmap["_beatmapFilename"])
            print(beatmap["_beatmapFilename"])
    for fname in difficulty_files:
        with open(fname, 'rb') as f:
            hash_obj.update(f.read())
    return hash_obj.hexdigest()

for song in local_songfolder.iterdir():
    if not is_song_hashed(song.name):
        hash = get_song_hash(str(song))
        info(f"Hashing {song.name} to {hash}")
        os.rename(song, str(song.parent) + "/" + hash)