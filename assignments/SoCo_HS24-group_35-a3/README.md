# 35-Assignment-3

Note: Alina Vanessa Brüllhardt and Z3lik0 are the same person


#### 1. **Assignment Structure: Division of Tasks**
Step 1: Yifu & Alina
    Yifu: Main code
    Alina: Bug fixes, refactoring, adding diff & checkout methods
    Lisa: .gitignore, bugfixes, refactoring
Step 2: Yifu & Alina
    Yifu: main(), etc.
    Alina: Init, diff & checkout method
    Lisa: .gitignore


------------------------------------------------------------------
## 2.1 Tig.py Implementation Usage Guide

------------------------------------------------------------------
### 1. Initialize Repository
```zsh
python tig.py init repo
```
**Output:**
Repository 'repo' created.
---------------------------
### 2. Create Files
```zsh
cd repo
echo "SoCo stands for Software Construction" > file.txt
echo "SoCo is a course this fall semester" > other_file.txt


python ../tig.py status
```
**Output:**
file.txt -- untracked
other_file.txt -- untracked
---------------------------
### 3. Stage Files
```zsh
python ../tig.py add file.txt
python ../tig.py stage other_file.txt #accepts both add and stage
python ../tig.py status
```
**Output:**
'file.txt' has been staged.

'other_file.txt' has been staged.

file.txt -- staged
other_file.txt -- staged
---------------------------

### 4. Initial Commit
```zsh
python ../tig.py commit "Initial commit: Stuff about SoCo"
python ../tig.py status
```
**Output:**
file.txt -- committed
other_file.txt -- committed
---------------------------

### 5. Modify Files
```zsh
echo "SoCo also stands for Scenes of Crime Officer" >> file.txt
python ../tig.py status
```
**Output:**
file.txt -- modified
other_file.txt -- committed

---------------------------
### 6. Check Differences
```zsh
python ../tig.py diff file.txt
```
**Output:**
```diff
--- file.txt	2024-11-27 16:52:41
+++ file.txt	2024-11-27 16:53:40
@@ -1 +1,2 @@
 SoCo stands for Software Construction
+SoCo also stands for Scenes of Crime Officer
```
---------------------------
### 7. Commit Changes
```zsh
python ../tig.py add file.txt
python ../tig.py commit "Updated definition of SoCo in other_file.txt"
```
---------------------------
### 8. View Commit Log
```zsh
python ../tig.py log
```
**Output:**
```
Log has only 2 entries. Showing all available entries:

commit id: 2
commit date: 2024-11-27 17:21:15
commit message: Updated definition of SoCo in other_file.txt

commit id: 1
commit date: 2024-11-27 17:20:44
commit message: Initial commit: Stuff about SoCo
```
---------------------------

### 9. Checkout First Commit
```zsh
python ../tig.py checkout 1
cat file.txt
python ../tig.py status
```
**Output:**
```
SoCo stands for Software Construction

file.txt -- modified
other_file.txt -- committed
```
------------------------------------------------------------------
## 2.2 Tig Java Implementation Usage Guide
------------------------------------------------------------------
Usage of Tig.java:
javac -cp lib/java-diff-utils-4.9.jar ../Tig.java (before cd repo_java)
java -cp ../:../lib/java-diff-utils-4.9.jar Tig <method> <argument>

### 1. Repository Initialization

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig init repo_java
```
**Output:**
```
Repository 'repo_java' created.
```

### 2. Creating Initial Files

```zsh
echo "SoCo stands for Software Construction" > file.txt
echo "SoCo is a course this fall semester" > other_file.txt
```

### 3. Checking Repository Status

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig status
```
**Output:**
```
file.txt -- untracked
other_file.txt -- untracked
```

### 4. Adding Files to Staging

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig add file.txt
java -cp ../:../lib/java-diff-utils-4.9.jar Tig add other_file.txt
```

### 5. Checking Status After Staging

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig status
```
**Output:**
```
file.txt -- staged
other_file.txt -- staged
```

### 6. Committing Changes

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig commit "Initial commit: Stuff about SoCo"
```

### 7. Modifying a File

```zsh
echo "SoCo also stands for Scenes of Crime Officer" >> file.txt
```

### 8. Checking Diff

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig diff file.txt
```
**Output:**
```
--- .tig/1/file.txt
+++ file.txt
@@ -2,0 +2,1 @@
+SoCo also stands for Scenes of Crime Officer
```

### 9. Viewing Commit Log

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig log
```
**Output:**
```
Commit Log
----------

commit ID: 2
commit Date: 2024-12-02
commit Message: 'Updated definition of SoCo in other_file.txt'

commit ID: 1
commit Date: 2024-12-02
commit Message: 'Initial commit: Stuff about SoCo'
```

### 10. Checking Out a Previous Commit

```zsh
java -cp ../:../lib/java-diff-utils-4.9.jar Tig checkout 1
```

### Usage Notes
- Ensure you have `java-diff-utils-4.9.jar` in your `lib` directory
- Run commands from the repository directory
- Use the classpath `-cp` option to include necessary libraries




------------------------------------------------------------------
3. **Explanation of the decisions taken in Step 2 - tig in Python** 
------------------------------------------------------------------


Yifu:
    To identify a file, we want to identify its name and content. To compare content more efficiently, we read the content of a file in its binary form and turn it into a *hash_code* by using *sha256(<file_content>).hexdigest()[:HASH_LEN]*, where *HASH_LEN* is set to 16. We store the file's name, *filename*, and its content, *hash_code*, into a dictionary as a key-value pair for easy access.

    We call such a dictionary a *manifest*, since it is essentially a snapshot of the files and their content. 

    We utilized manifests to identify the status of a file. When adding a file, we are actually adding its *filename*, *hash_code* pair into a manifest, and when we check the status of a file, we lookup the file's name inside the manifest. If the file is there, then we know the file is added, and therefore is 'staged'.

    Similarly, when doing commit, we create a manifest for that particular commit, and for all the staged files, we add their *filename*, *hash_code* pairs into that manifest. The manifest, along with *commit_id*, *commit_date*, and *commit_message* are stored into a bigger dictionary for later use. All of such dictionaries for all the commits are stored in a list, which becomes the *commit_log*. When checking a file's status, we go into the latest entry of the *commit_log* and look at its manifest, if we can find the file in the manifest, we know the file is committed. When we commit, we also copy all of the staged files into a backup directory inside *.tig/*. The name of the backup directory is the *commit_id* of that particular commit.

    Since we need to handle multiple command line prompts, *tig* must store relevant information locally in order to access it in the future. We store the manifest for staged files and the *commit_log* in json format into the *.tig/* directory. They are named *staged.json* and *commit_log.json* respectively. 

    Each time we check the status of the files, we also want to learn if a committed file's content is modified. To do that, we only need to compare the *hash_code* of the content of the file right now and that at the last commit. If the hash_code is different, we change the status of that file to 'modified'.

Alina: 
    Minor Fixes and Refactoring
    - Modified `init()` method to create the repository directory if it doesn't exist
    - Path handling using `pathlib.Path` as opposed to using strings
    - Replaced if-statements with match-block for improved readability
    - Added 'stage' as alternative keyword for `add()` method 
    - Modified `current_date()` function to include time, affects manifest and diff function
    - Added to log function: displays all log entries if log is shorter than default, otherwise default or user-specified value

    Diff Command
    - Implemented `diff()` method to show changes between current and most recent file version 
        - loops through manifest to find most recent commit
        - Uses `unified_diff()` module for generating the comparison according to the unified diff format

    Checkout Command
    - Added `checkout()` method to restore repository state to a specific commit-id's state
    - Verifying commit ID existence
    - Looping through current working directory to delete all existing files (except .tig directory)
            For simplicity it was assumed that we only need to consider files (like in the use case), not folders. Therefore only one loop was implemented (for files), folders were ignored.
    - Paths are created from file_location.json file, that indicates where the most current version at each commit is (each commit has its own)
    - Copying files from the specified commit-id's folder using shutil.copy2
        - Again, it was assumed that only files had to be moved, as per use case.

------------------------------------------------------------------
4. **Explanation of the decisions taken in Step 2 - tig in Java** 
------------------------------------------------------------------


Diff: 
    - Implemented `diff()` method to show changes between current and most recent file version 
        - uses helper method findHighestCommitId to find the most recent commit ID folder to check its FileLocation.json <- this file states which commit version the most up to date is for each file up until this commit
        - Uses the FileLocation.json to create Path for the previous file that we want to compare the current one to
        - makes use of createUnifiedDiff() to create the unified Diff String
            - modified the code provided by ChatGPT to handle the case where there is no difference
        - prints this String to console 


Checkout: 
    - checkout method first creats the (potential) paths for the commit-id directories to then check whether they exist
    - if they exist, the fileLocations.json inside that directory contains the location for all files newest version up until that commit 
    - we then delete all files in the current directory (repo)
    - parsing the file.Locations.json gives us the paths we need to copy the right files back to the current directory

------------------------------------------------------------------
#### 5. **Use of Generative AI**
------------------------------------------------------------------


Used terminal output & Claude.AI to generate markdown version of #Tig Use Case Demonstration for better legibility.

ChatGPT / Claude.AI: 
- Asked how to read and write to JSON files in Java. *StagedWriter*, *CommitWriter* class are written with the help of ChatGPT.
- Used ChatGPT & Claude to coach me through all the Java bits and changed the generated input to fit our project bettter  - Alina
    - finding best unified diff library in Java & going through the import steps
    - Javafying my python code, asking for python snippet equivalents in Java
    - asked to generate helper methods findHighestCommitId() and Unified Diff library method createUnifiedDiff()
    - Help with debugging / understanding error messages 
    - Asking to explain some code written by group members (primarily in Java) or code snippets it generated from my javafying prompts

