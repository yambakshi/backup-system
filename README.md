# Backup System
Backup system for backing up Google Drive files and local files.

This project was generated with:
- Python version: 3.9.0

## Installing & Running
### Setup
1. Open `cmd` and navigate to the projects folder:
```
cd "Python Projects"
```

2. Create project folder:
```
mkdir "Backup System"
```

3. Clone repo into project folder `Backup System`:
```
git clone https://github.com/yambakshi/backup-system.git .
```

4. Create project virtual environment `env`:
```
python -m venv env
```

5. Open `VSCode` in project folder:
```
code .
```

6. In `VSCode` create `src` folder in the project directory:
```
mkdir src
```

7. Create `main.py` in `src` folder in order for `VSCode`'s python extension to recognize the `env` virtual environment and set its interpertor to the `venv`'s interperter:
```
touch main.py
```

8. In order to activate the `venv` in `VSCode`'s terminal you'll first need to enable running powershell scripts.
   1. First check what's the current policy by running:
   ```
   get-executionpolicy
   ```
   2. The output should be `Restricted` which is the default policy that's preventing you from running the `venv` activation script that's located in:
   ```    
   env/Scripts/Activate.ps1
   ```
   3. To change the execution policy run:
   ```
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   4. Then activate `venv` by running:
   ```
   env/Scripts/Activate.ps1
   ```
   5. Deactivate the `venv` by running:
   ```
   deactivate
   ```

### Requirements
#### Install Requirements
1. Before installing the requirements, make sure that the `venv` is activated (notice the `(env)` in the beginning):
```
(env) PS D:\Yam Bakshi\Careers\Hi-Tech\Portfolio\Python\Backup System >
```
2. Install `requirements.txt` packages:
```
pip install -r requirements.txt
```
#### Updating Requirements
Updating `requirements.txt` with currently installed `pip` packages (-l or --local flag to save only local packages and not global):
```
pip freeze -l > requirements.txt
```


### Google API Authentication
The `Google API` authentication is done with the `./authentication/credentials.json` file.
The first time you authenticate, a `token.pickle` file will be generated and saved in the `./authentication` folder.
The `token.pickle` will expire after some time, so you'll have to delete it manually in order for a new one to be generated:
```
rm -rf ./authentication/token.pickle
```

### VSCode Python Interpreter
To select the `venv`'s interperter in `VSCode`:
1. Hit `Ctrl`+`Shift`+`P`.
2. Type `Python: Select Interpreter` and hit `Enter` to edit the setting.
3. Select `Python 3.9.0 ('env':venv) '.\env\Scripts\python.exe`.

### Run
- `Google Drive` backup to local drive `D:/`
```
python ./src/main.py --local
```
- `Local` backup to external drive `F:/`
```
python ./src/main.py --google-drive
```

Add merge_diff param

## Terms & Walkthrough
### Spaces
There are 3 spaces:
- local - `D:/`
- drive_stream - `G:/`
- drive - `Google Drive`

### Caches
Scans are cached so that you won't have to scan all 3 spaces everytime you want to backup.
If you'd like to load the scans caches in your next backup instead of re-scanning, simply set the `load_cache` member of the `backup_system` class to `True` (default is `False`).

### Snapshots
What are snapshots?

### Diff
There are 3 diff types:
1. `new` - Files that exist in `Google Drive` but don't exist in `D:/` in the same paths.
2. `modified` - Files that exist on the same paths both in `Google Drive` and in `D:/` but that their `last_modified` is different.
3. `removed` - Files that don't exist in `Google Drive` but exist in `D:/` in the same paths.

### File Types
There are currently 3 suppoerted file types:
1. Google Doc
2. Google Sheet
3. PDF

### Step-by-Step: Google Drive Backup
Upon running the Backup System with the `--google-drive` flag, the backup system will:
1. Scan all 3 spaces, or load the scans caches if `load_cache` is `True`.
2. Compare the scans.
3. Download `new` and `modified` files from `Google Drive` and saves them in a `./tmp` folder under their correlating paths.
4. Merge the diff into the local `D:/` drive, as follows:
   1. `new` - Moves the downloaded files from the `./tmp` folder to their destination folders.
   2. `modified` - Moves the downloaded files from the `./tmp` folder to their destination folders replacing the old files.
   3. `removed` - Deletes from the local `D:/` drive.
5. Finally, save snapshots of the current files state for future comparisons.