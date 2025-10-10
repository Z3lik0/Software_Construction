import json
from difflib import unified_diff
import sys


def find_ver(filename):
    with open("log.json", "r") as f:
        data = json.load(f)
        print(data)

        counter = 0
        file_vers = {}

        for i in reversed(range(len(data))): #checking backwards from the most recent one
            id = (data[i]["commit_id"])
            manifest = data[i]["manifest"]

            if counter == 2: 
                return 

            if filename in manifest.keys():
                file_hash = manifest[filename]
                counter += 1
    return filename, file_hash




    #print(len(data)) #could be the same or diff - if diff, do the diff thing
filename = "file.txt"
find_ver(filename)

