from pathlib import Path
from glob import glob
from hashlib import sha256
from time import time
import shutil
import sys


def backup(source_dir, backup_dir):
    manifest = hash_all(source_dir)
    timestamp = current_time()
    write_manifest(backup_dir, timestamp,manifest)
    copy_files(source_dir, backup_dir, manifest)
    return manifest

def current_time():
    return f"{time()}".split(".")[0]

def hash_all(dir, HASH_LEN = 16):
    result = []
    for name in glob("**/*.*", root_dir = dir, recursive = True): #"**/*.*" stars mean you match anything (all paths, all filenames, all file extensions)
        full_name = Path(dir, name)
        with open(full_name, "rb") as f: #read them as binary (rb)
            data = f.read()
            hash_code = sha256(data).hexdigest()[:HASH_LEN]


def write_manifest(backup, timestamp, manifest):
    #check the backup dir exists, if not: create
    backup_dir = Path(backup)
    if not backup_dir.exists():
        backup_dir.mkdir()
    
    manifest_file = Path(backup_dir, timestamp+".csv")
    with open(manifest_file, "w") as f:
        #f.writelines(manifest) #manifest is list
        f.writelines("filename, hash"+ "\n")
        for filename, hash_code in manifest:
            f.write(filename + "," + hash_code + "\n")

def copy_files(source_dir,backup_dir, manifest):
    for (filename, hash_code) in manifest: #filename (hello.txt), hashcode ()
        source_path = Path(source_dir, filename) #constructs path of file based on filename (hello.txt)
        backup_path = Path(backup_dir, hash_code) #constructs path of backupfile via filename (which here is the hashcode)
        if not backup_path.exists(): #if the file with the hashname doesn't exist:
            shutil.copy(source_path, backup_path)  #we make it exist. (we create the copy)

    

if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: backup.py source_dir dest_dir"
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    backup(source_dir,dest_dir)
