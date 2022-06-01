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
from pathlib import Path, PurePosixPath
local_songfolder = Path(r"G:\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels")
remote_songfolder = PurePosixPath("/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/")

ls_result = []
from ppadb.client import Client as AdbClient
def dump_shell(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print(data.decode('utf-8'))
    connection.close()
def dump_shell_by_line(connect):
    file_obj = connect.socket.makefile()
    for index in range(0, 10):
        print("#{}: {}".format(index, file_obj.readline().strip()))
        
def ls_by_line(path):
    return check_output(["adb","shell",f"ls \"{path}\""]).decode().splitlines()
        
client = AdbClient(host="127.0.0.1", port=5037)
device = client.devices()[0]

def exec(cmd=""):
    warning(f"Executing: {cmd}")
    device.shell(cmd, handler=dump_shell)
def rm(path): exec(f"rm -f -rR -v \"{path}*\"")
def ls_song_folder(add = ""): exec(f"ls {remote_songfolder / add}")
def mkdir(path): exec(f"mkdir -p \"{path}\"")

def push(cur, max, src, dst):
    info(f"[{cur}/{max}] Pushing \"{src}\"\nto \"{dst}\"")
    device.push(src, dst)

def is_song_hashed(song_dir_name):
    return True if match(r'[0-9a-f]{40}', song_dir_name) else False

import os
from fnmatch import filter
def get_info_dat(song_dir: str): return song_dir + "/" + filter(os.listdir(song_dir), '[Ii][Nn][Ff][Oo].[Dd][Aa][Tt]')[0]
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

songs = []
uploaded_songs = ls_by_line(remote_songfolder)

# for song in uploaded_songs:
#     rm(remote_songfolder / song)
# exit(0)
i = 0
for song in local_songfolder.iterdir():
    if song.name in uploaded_songs or (is_song_hashed(song.name) and get_song_hash(str(song)) == song.name): i += 1
    else: songs.append(song)
l = len(songs)
info(f"Found {l} songs to upload (Skipping {i} already uploaded songs)")

i = 0
for song in songs:
    i += 1
    src = str(song)
    dst = str(remote_songfolder / song.name)
    try:
        # push(i, l, src + "/.", dst)
        mkdir(dst)
        for file in song.iterdir(): push(i, l, str(file), dst + "/" + file.name)
        # sleep(.1)
        # ls_song_folder(song.name)
    except Exception as e:
        error(f"Could not push \"{song.name}\": \"{e.args[0]}\"")

ls_song_folder()

client.remote_disconnect()