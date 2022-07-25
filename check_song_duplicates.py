print("start")

from pathlib import Path
from shutil import rmtree
from hashlib import md5
from json import load as json_load

root = Path(r"G:\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels")

# iterate over subfolders in root

def print_dir(_path: Path):
    print(f"- \"{_path.name}\"")
    for obj in child.iterdir():
        if not str(obj).lower().endswith(".dat"): print(f" - \"{obj.name}\"")

def get_song_files(_path: Path):
    song_files = [Path(), []]
    info_file = _path / "info.dat"
    if info_file.is_file():
        with open(info_file, "r") as f:
            json = json_load(f)
            if json:
                song_files[0] = _path / json["_songFilename"]
    
    song_files[1] += list(_path.glob("*.ogg"))
    song_files[1] += list(_path.glob("*.egg"))
    song_files[1] += list(_path.glob("*.mp3"))
    return song_files

def get_md5(_path: Path):
    with open(_path, "rb") as f:
        file_hash = md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
        return file_hash.hexdigest()

hashes = {}
childs = list(root.iterdir())
print(len(childs), "childs found")
for child in childs:
    if not child.is_dir(): continue
    # if child.name.endswith(".FullName"): child.rename(child.parent / child.name.replace(".FullName", ""))
    song_file, song_files = get_song_files(child)
    if not song_files:
        print(f"No song file found in {child.name}!")
        # rmtree(child)
        continue
    elif not song_file.is_file():
        print(f"Song file mismatch in {child.name}!")
        print(f"{song_file.name} -> {song_files[0].name}")
        print_dir(child)
    elif len(song_files) > 1:
        print(f"Multiple songs found in {child.name}!")
        for file in song_files:
            print(f"=>{file.name}")
        for file in song_files[1:]:
            if file.name != song_file.name:
                print(f"Deleting unmatching {file.name}")
                file.unlink()
        continue
    # calculate md5 hash of song_file
    song_hash = get_md5(song_files[0])
    print(f"Song {child.name} has song file {song_file.name} ({song_hash})")
    # print(f"{child.name} - {song_hash}")
    if not song_hash in hashes.keys(): hashes[song_hash] = []
    hashes[song_hash].append(child)
print(len(hashes), "hashes found")
for hash, songs in hashes.items():
    if len(songs) > 1:
        print("Duplicate songs found:")
        for song in songs:
            print(f" - {song.name}")
            if not ' ' in song.name:
                print("Deleting duplicate song without whitespace:", song.name)
                # rmtree(song)
print("end")