from glob import glob
from pathlib import Path
from hashlib import sha256
import sys
import json
from datetime import datetime
import shutil
from difflib import unified_diff


HASH_LEN = 16

class Tig:
    def __init__(self):
        self.repo_dir = None

    def init(self, repo_name):
        """
        Initialize a folder as our repository and create .tig/ folder inside. 

        Parameters
        ----------
        repo_dir: The name of the repository directory.

        Returns
        -------
        Returns 0 if the repo directory already exist.
        Returns the path to .tig/ if the repo directory is created successfully. 
        
        """
        folder_path = Path(repo_name)
        if not folder_path.exists():
            # print(f"Error: Repository '{repo_name}' does not exist.\n")
            # return 0
            folder_path.mkdir()
        tig_path = Path(repo_name).joinpath(".tig")
        if tig_path.exists():
            print(f"Error: {tig_path} already exists!\n")
            return 0
        else:
            tig_path.mkdir()
        print(f"Repository '{repo_name}' created.\n")
        return tig_path


    def get_tig_ignore(self):
        tig_ignore_path = Path(".tig", ".tigignore.*")
        
        if not tig_ignore_path.exists():
            return []
        
        lines = tig_ignore_path.read_text().splitlines()
        
        return [line.strip() for line in lines if line.strip() and not line.startswith("#")]



    def add(self, filename):
        """
        Move <filename> to the staged state. 
        Write filename, hash_code pair into a dictionary in
        'staged.json' to indicate the file is staged

        Parameter
        ---------
        filename: the name of the file that is to be staged

        Return
        -------
        returns the (filename, hash_code) tuple
        """
        staged_path = Path(".tig") / "staged.json"

        # Check if stage file already exist,
        # if so, read the existing dictionary into 'data'
        # if not, create it and create an empty dictionary as 'data'.
        if staged_path.exists():
            content = staged_path.read_text().strip() #first read it without assuming a structure
            if content:  #if the file is not empty
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    print("Error: staged.json contains invalid JSON.")
                    data = {}
            else:
                data = {}
        else:
            data = {}
            staged_path.write_text(json.dumps({}, indent=4)) 
                
        if filename in self.get_tig_ignore():
            return 0
        
        
        for name in glob("**/*.*", root_dir=self.repo_dir, recursive=True):
            if name == filename:
                # Put the file's filename, hash_code
                # into the dictionary as a key-value pair
                new_data_dict = {filename: self.hash_file(filename)}
                data.update(new_data_dict)
                # write the updated dictionary back into the stage file.
                staged_path.write_text(json.dumps(data, indent=4))
                print(f"'{filename}' has been staged.\n")
                return (filename, self.hash_file(filename))

        print(f"Error: File '{filename}' cannot be found!\n")
        return 0

    def commit(self, message):
        """
        Commit all staged files so that they are saved permanently in the repository's history.
        Each commit stores all staged files with a unique identifier, a timestamp, and a commit message.
        Each commit generates a commit folder that stores all the staged files along with a 
        snapshot of all committed files, along with the identifier, timestamp, and the commit message.

        Parameters
        ----------
        message: commit message written in natural language.

        Return
        ------ 
        Returns the commit id.
        """
        commit_id = None
        date = self.current_date()
        log_path = Path(".tig") / "commit_log.json"


        # Check if the commit log exists,
        # if so, read the most recent id from the commit log,
        # if not, create the commit log
        # Update log when committing
        # 'log' is a list of dictionaries each containing
        # the commit_id, commit_date, and the commit_message of a commit.
        # It is stored in json
        if log_path.exists():
            log = json.loads(log_path.read_text())
            commit_id = int(log[-1]["commit_id"]) + 1
        else:
            log = []
            commit_id = 1
        # Create a file_location dictionary for file_location inside the <commit_id> directory
        # It will tell us where the files are stored for each commit
        # an entry of the dictionary will look something like "'file.txt': 1",
        # where 1 is the commit id of the latest commit for file.txt
        previous_commit_id = str(commit_id - 1)
        previous_note_path = Path(".tig") / previous_commit_id / "file_location.json"
        if previous_note_path.exists():
            file_location = json.loads(previous_note_path.read_text())
        else:
            file_location = {}

        # Commit all staged files by moving them to the committed state
        # by copying the manifest in 'staged.json' to the commit log
        staged_path = Path(".tig") / "staged.json"
        if staged_path.exists():
            manifest = json.loads(staged_path.read_text())
        else:
            manifest = {}
        # update file_location dictionary according to the manifest. 
        for file in manifest:
            entry = {file: commit_id}
            file_location.update(entry);
        # Save all staged files to the 'commit_dir' directory.
        commit_dir = Path(".tig") / str(commit_id)
        if commit_dir.exists():
            pass
        else:
            commit_dir.mkdir()
    
        # print(f"DEBUG: manifest: {manifest}\n")
        for filename in manifest:
            source_path = Path(".") / filename
            backup_path = Path(".tig")/ str(commit_id)/ filename
            if not backup_path.exists():
                shutil.copy(source_path, backup_path)
        # Carry over the manifest from the last commit
        # to include the committed files from the previous commits
        if commit_id > 1:
            # print(f"DEBUG: commit(): log: {log}\n")
            # print(f"DEBUG: commit(): log[commit_id - 2]: {log[commit_id - 2]}\n")
            # print(f"DEBUG: commit(): log[commit_id - 2]['manifest']: {log[commit_id - 2]['manifest']}\n")
            old_manifest = log[commit_id - 2]["manifest"].copy()
        else:
            old_manifest = {}
        # print(f"DEBUG: commit(): manifest from staged: {manifest}\n")
        # print(f"DEBUG: commit(): manifest from previous commit: {old_manifest}\n")
        old_manifest.update(manifest)
        manifest = old_manifest
        # print(f"DEBUG: commit(): updated manifest: {manifest}\n")

        # Update the log
        log.append({
            "commit_id": commit_id,
            "commit_date": date,
            "commit_message": message,
            "manifest": manifest
        })
        log_path.write_text(json.dumps(log, indent=4))

        # Create a commit file_location inside the commit_id directory
        file_location_path = Path(".tig")/str(commit_id) / "file_location.json"
        file_location_path.write_text(json.dumps(file_location, indent=4))

        # After copying the manifest from staged, we wipe staged.json clean,
        # thus moving the relevant files from staged to committed.
        staged_path.write_text(json.dumps({}, indent=4))
        return commit_id

    def status(self):
        """
        Check if a file is modified:
        A file that is not untracked and has changed since the last commit.

        Show the status of all the file(s) in the repository.
        """
        staged_path = Path(".tig") / "staged.json"
        log_path = Path(".tig") / "commit_log.json"
        if staged_path.exists():
            staged_dict = json.loads(staged_path.read_text())
        else:
            staged_dict = {}
        if log_path.exists():
            manifest = json.loads(log_path.read_text())[-1]["manifest"]
        else:
            manifest = {}
        # DEBUG: Show all files in repo
        for name in glob("**/*.*", root_dir=".", recursive=True):
            if name in self.get_tig_ignore():
                pass
            
            if name in staged_dict:
                print(f"{name} -- staged")
            elif name in manifest:
                if self.hash_file(name) == manifest[name]:
                    print(f"{name} -- committed")
                else:
                    print(f"{name} -- modified")
            else:
                print(f"{name} -- untracked")

    def log(self, N = "-5"):
        """
        Print out the last N log entries

        Parameter:
        N: number of entries in the form of a string following a dash i.e. '-2'
        """
        log_path = Path(".tig") / "commit_log.json"
        # Check if the path exists
        if log_path.exists():
            log = json.loads(log_path.read_text())
        else:
            print("Error: log does not exist yet.")
            return 0
        # Take off the '-' in front of 'N'
        N = N[1:]
        # Check if N is numeric
        if not N.isnumeric():
            print(f"Error: argument provided must be a number! Argument provided is '{N}'\n")
            return 0
        else:
            N = int(N)
            # Check if N is numeric is bigger then the number of entries in the log
            if len(log) < N:
                N = len(log)
                print(f"Log has only {len(log)} entries. Showing all available entries:\n")                # )

            for i in range(N):
                print(
                    f"commit id: {log[-i-1]['commit_id']}\n"\
                    f"commit date: {log[-i-1]['commit_date']}\n"\
                    f"commit message: {log[-i-1]['commit_message']}\n"\
                    )




    def diff(self, filename):
    
        commit_log_path = Path(".tig") / "commit_log.json"
        with commit_log_path.open("r") as f: 
            data = json.load(f)
        
        commit_id_found=None
        for i in reversed(range(len(data))):
            manifest = data[i]["manifest"]
            if filename in manifest.keys():
                commit_id_found=str(i+1)
                commit_date = data[i]["commit_date"]
                break
                
        if commit_id_found==None:
            print(f"file {filename} was never commited")
            return 0
        
        location_json_path = Path(".tig")/commit_id_found/"file_location.json"
        with location_json_path.open("r") as f: 
            location_json = json.load(f)
        
        commit_id_found=str(location_json[filename])
        
        path_committed = Path(".tig") / commit_id_found / filename
        path_new=Path(filename)
        
        with path_new.open() as new_file, path_committed.open() as committed_file:
            new = new_file.readlines()
            committed = committed_file.readlines()

        delta = unified_diff(committed, new, filename, filename, commit_date, self.current_date())
        sys.stdout.writelines(delta)
        


    def checkout(self, commit_id):
        '''
        Restore the directory's files to the state of a specific commit ID.
            Usage: python3 tig.py checkout <commit id>


        Parameter
        ----------
        commit-id: name of commit state should be reverted to.

        Returns
        ----------
        None
        '''

        
        file_locations = Path(".tig") / str(commit_id) / "file_location.json"
        dest_dir = Path.cwd()
        commit_dir = Path(".tig") / str(commit_id)
        assert Path.is_dir(commit_dir), "Invalid commit ID."


        with file_locations.open("r") as f: 
            data = json.load(f)

        #delete all previous files in repo except .tig
            for file in dest_dir.iterdir(): #iterable object with all files
                if file.is_file(): #assuming we're only supporting files, no folders
                    file.unlink()
            
        for entry in data.items(): #list of tuples
            filename, version = entry

            source_file = Path(".tig") / str(version) / filename #gets the file from the last commit-id folder

            dest_path = dest_dir / filename
            if source_file.exists():
                shutil.copy2(source_file, dest_path)
            else:
                print(f"Warning: Source file {source_file} not found for {filename}, version {version}")
            

    def hash_all(self, root):
        '''
        Takes a snapshot of all the content in the root directory and returns the snapshot as a manifest

        Parameters
        ----------
        root: a string representing the path to the directory you want to take the snapshot

        Returns
        -------
        A list of tuples (name, hash_code):
        'name' is a string representing the path to file from root. It can be 'a.txt' or 'subdir/b.txt'
        'hash_code' is 'sha256({file content}).hexdigest()[:HASH_LEN]'
        '''
        result = []
        for name in glob("**/*.*", root_dir=root, recursive=True):
            full_name = Path(root, name)
            with open(full_name, "rb") as reader:
                data = reader.read()
                hash_code = sha256(data).hexdigest()[:HASH_LEN]
                result.append((name, hash_code))
        return result

    def hash_file(self, filename):
        """
        Takes a snapshot of a file and returns the snapshot as a manifest

        Parameters
        ----------
        root: a string representing the path to the directory you want to take the snapshot

        Returns
        -------
        A tuple (name, hash_code):
        'name' is a string representing the path to file from root. It can be 'a.txt' or 'subdir/b.txt'
        'hash_code' is 'sha256({file content}).hexdigest()[:HASH_LEN]'
        """
        file_path = Path(filename)
        with open(file_path, "rb") as reader:
            data = reader.read()
            hash_code = sha256(data).hexdigest()[:HASH_LEN]
            return hash_code

    def current_date(self):
        """
        Returns the current date as a string.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    

        

def main():
    """
    Handles all the command line arguments.
        sys.argv[0]: The script name (tig.py).
        sys.argv[1]: The command (e.g., init, add).
        sys.argv[2]: The arguments for the command.
    """
    if len(sys.argv) < 2:
        print("Error: No command provided\n")
        sys.exit(1)

    command = sys.argv[1]

    if len(sys.argv) < 3 and command != 'status' and command != 'log':
        print(f"Error: '{command}' command requires more argument.\n")
        sys.exit(1)

    tig = Tig()
    if command == "init":
        return_value = tig.init(sys.argv[2])
    elif command in ["add", "stage"]:
        return_value = tig.add(sys.argv[2])
    elif command == "commit":
        return_value = tig.commit(sys.argv[2])
    elif command == "log":
        if len(sys.argv) == 3:
            return_value = tig.log(sys.argv[2])
        else:
            return_value = tig.log()
    elif command == "diff":
        return_value = tig.diff(sys.argv[2])
    elif command == "status":
        return_value = tig.status()
    elif command == "checkout":
        return_value = tig.checkout(sys.argv[2])
    else:
        print(f"Error: Unknown command: '{command}'\n")


if __name__ == "__main__":
        main()
