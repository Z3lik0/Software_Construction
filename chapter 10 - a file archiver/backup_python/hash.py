from glob import glob
from pathlib import Path
from hashlib import sha256




def hash_all(dir, HASH_LEN = 16):
        result = []
        for name in glob("**/*.*", root_dir = dir, recursive = True): #"**/*.*" stars mean you match anything (all paths, all filenames, all file extensions)
            full_name = Path(dir, name)
            with open(full_name, "rb") as f: #read them as binary (rb)
                data = f.read()
                hash_code = sha256(data).hexdigest()[:HASH_LEN]