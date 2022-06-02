import hashlib
from re import match
from subprocess import check_output
from time import sleep
from logging import *
from json import load
from shutil import rmtree, copy
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
local_songhashfile = local_songfolder / 'hashes.txt'
import os
from fnmatch import filter
def get_info_dat(song_dir: str): return song_dir + "/" + filter(os.listdir(song_dir), '[Ii][Nn][Ff][Oo].[Dd][Aa][Tt]')[0]
def get_song_info(song_info_file: str):
    with open(str(song_info_file), 'r') as info_dat: return load(info_dat)
def is_song_hashed(song_dir_name): return True if match(r'[0-9a-f]{40}', song_dir_name) else False

def get_song_filename(song_dir):
    song_info = get_song_info(get_info_dat(str(song_dir)))
    return f'[BSD] {song_info["_songName"]} - {song_info["_songAuthorName"]}'
def merge(scr_path, dir_path):
  files = next(os.walk(scr_path))[2]
  folders = next(os.walk(scr_path))[1]
  for file in files: # Copy the files
    scr_file = scr_path + "/" + file
    dir_file = dir_path + "/" + file
    if os.path.exists(dir_file): # Delete the old files if already exist
      os.remove(dir_file)
    copy(scr_file, dir_file)
  for folder in folders: # Merge again with the subdirectories
    scr_folder = scr_path + "/" + folder
    dir_folder = dir_path + "/" + folder
    if not os.path.exists(dir_folder): # Create the subdirectories if dont already exist
      os.mkdir(dir_folder)
    merge(scr_folder, dir_folder)

local_songhashfile = open(str(local_songhashfile), 'w', encoding="utf-8")
for song in local_songfolder.iterdir():
    if is_song_hashed(song.name):
        try:
            unhashed_name = get_song_filename(str(song))
            local_songhashfile.write(f'{song.name}=\"{unhashed_name}\"\n')
            info(f"Unhashing {song.name} to {unhashed_name.encode('utf-8')}")
            dst = f"{str(song.parent)}/{unhashed_name}"
            try: os.rename(song, dst)
            except FileExistsError:
                warning(f"Merging {song.name}")
                merge(song, dst)
                # rmtree(song, True)
        except PermissionError as e: print(e)
local_songhashfile.close()