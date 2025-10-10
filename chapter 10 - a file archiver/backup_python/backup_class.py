from time import time
import sys
from pathlib import Path
import shutil

from hash import hash_all

class Archive():
    def __init__(self, source_dir):
        self._source_dir = source_dir
     
    def _current_time(self):
        return f"{time.time()}".split(".")[0]
    
    def _write_manifest():
        raise NotImplementedError
    
    def _copy_files():
        raise NotImplementedError
    
    def backup(self,dest_dir):
        manifest = hash_all(self.source_dir)
        timestamp = self._current_time()
        self._write_manifest(dest_dir, timestamp, manifest)
        self._copy_files(source_dir, dest_dir, manifest)
        return manifest
    
class LocalArchive(Archive):
    def __init__(self, source_dir):
        super().__init__(source_dir)

    def _write_manifest(self, backup_dir, timestamp, manifest):
        #check the backup dir exists, if not: create
        backup_dir = Path(backup_dir)
        if not backup_dir.exists():
            backup_dir.mkdir()
        
        manifest_file = Path(backup_dir, timestamp+".csv")
        with open(manifest_file, "w") as f:
            #f.writelines(manifest) #manifest is list
            f.writelines("filename, hash"+ "\n")
            for filename, hash_code in manifest:
                f.write(filename + "," + hash_code + "\n")

    def _copy_files(self, dest_dir, manifest):
        for (filename, hash_code) in manifest: #filename (hello.txt), hashcode ()
            source_path = Path(self._source_dir, filename) #constructs path of file based on filename (hello.txt)
            backup_path = Path(dest_dir, hash_code) #constructs path of backupfile via filename (which here is the hashcode)
            if not backup_path.exists(): #if the file with the hashname doesn't exist:
                shutil.copy(source_path, backup_path)  #we make it exist. (we create the copy)
        
class RemoteArchive(Archive):
    pass

if  __name__ == "__main__":
    #assert len(sys.argv) == 3, "Usage: backup.py "
    assert len(sys.argv) == 3, "Usage: backup.py source_dir dest_dir"
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    
    archiver = LocalArchive(source_dir)
    archiver.backup(dest_dir)

         