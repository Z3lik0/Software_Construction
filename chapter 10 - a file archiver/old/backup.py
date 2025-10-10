import datetime

def hash_all(manifest):
    pass

def current_time():
    return datetime.today()

def write_manifest(backup_dir, timestamp, manifest):
    pass

def copy_files(source_dir, backup_dir, manifest):
    pass

def backup(source_dir, backup_dir):
    # manifest = csv file where first row: title, second row: hash
    # manifest should be named after something like date & time created 
    manifest = hash_all(source_dir)
    timestamp = current_time() #just another string like 202410161253 <- 2024.10.16. 12:53
    write_manifest(backup_dir, timestamp, manifest)
    copy_files(source_dir, backup_dir, manifest)
    return manifest


source_dir = "swcons"
backup_dir = "swcons_bkp"

