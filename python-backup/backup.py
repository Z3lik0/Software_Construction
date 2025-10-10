import sys
import os
import time
import shutil
from glob import glob
from pathlib import Path
from hashlib import sha256

HASH_LEN = 16


def backup(source_dir,backup_dir):
    manifest = hash_all(source_dir)
    timestamp = current_time() #string 202410161253
    write_manifest(backup_dir,timestamp,manifest)
    copy_files(source_dir,backup_dir,manifest)
    return manifest

def hash_all(dir):
    result = []
    for name in glob("**/*.*", root_dir=dir, recursive=True):
        full_name = Path(dir,name)
        with open(full_name,"rb") as f:
            data = f.read()
            hash_code = sha256(data).hexdigest()[:HASH_LEN]
            result.append((name,hash_code))
    return result # [(file.txt,sdajfhg238756),(sub/file2.txt,348576bkfwar)]


def current_time():
    return f"{time.time()}".split(".")[0]


def write_manifest(backup_dir,timestamp,manifest):
    backup_dir = Path(backup_dir)
    if not backup_dir.exists():
        backup_dir.mkdir()
    manifest_file = Path(backup_dir, timestamp+".csv")
    with open(manifest_file,"w") as f:
        f.write("filename,hash"+"\n")
        for filename,hash_code in manifest:
            f.write(filename + "," + hash_code + "\n")


def copy_files(source_dir,backup_dir,manifest):
    for (filename,hash_code) in manifest: # helo.txt, 0b8e6c43ac411146
        source_path = Path(source_dir,filename) # /Users/sback/soco/helo.txt
        backup_path = Path(backup_dir,hash_code) # /Users/sback/soco_bkp2/0b8e6c43ac411146
        if not backup_path.exists():
            shutil.copy(source_path,backup_path)



if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: backup.py source_dir dest_dir"
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    backup(source_dir,dest_dir)