# Backup System
Backup system for `Google Drive` and local files.

## Technologies
- Python 3.9.0

## Setup
### 1. Virtual Environment
1. Create the project's virtual environment `env` by running the following in the repo's root directory:
```
python -m venv env
```
2. Check the current execution policy (in order to activate the `venv` in `VSCode`'s terminal you'll first need to enable running powershell scripts):
```
get-executionpolicy
```
3. The default execution policy, `Restricted`, is preventing you from running the `venv` activation script that's in:
```    
env/Scripts/Activate.ps1
```
4. Set the execution policy for the current user to `RemoteSigned`:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
5. Activate the `venv`:
```
env/Scripts/Activate.ps1
```
**Usefull Commands**
- Deactivate the `venv`:
```
deactivate
```

### 2. Requirements
1. Before installing the requirements, make sure that the `venv` is activated (notice the `(env)` in the beginning):
```
(env) PS D:\Yam Bakshi\Careers\Hi-Tech\Portfolio\Python\Backup System >
```
2. Install `requirements.txt` packages:
```
pip install -r requirements.txt
```
**Useful Commands**
- Updating `requirements.txt` with currently installed `pip` packages (-l or --local flag to save only local packages and not global):
```
pip freeze -l > requirements.txt
```


### 3. Google API Authentication
The `Google API` authentication is done with the `./authentication/credentials.json` file.

The first time you authenticate, a `token.pickle` file will be generated and saved in the `./authentication` folder.

The `token.pickle` will expire after some time, so you'll have to delete it manually in order for a new one to be generated:
```
rm -rf ./authentication/token.pickle
```

### 4. VSCode Python Interpreter
To select the `venv`'s interperter in `VSCode`:
1. Hit `Ctrl`+`Shift`+`P`.
2. Type `Python: Select Interpreter` and hit `Enter` to edit the setting.
3. Select `Python 3.9.0 ('env':venv) '.\env\Scripts\python.exe`.

### 5. Run
```
python ./src/main.py --google-drive
## or
python ./src/main.py --local
```

## Knowledge Base
### Flags
There are 2 flags you can pass to the Backup System:
- `--google-drive` - Backup `Google Drive` files to local drive `D:/`
- `--local` - Backup local files to external drive `F:/`

### Spaces
There are 3 spaces:
- local - `D:/`
- drive_stream - `G:/`
- drive - `Google Drive`

### Caches
Scans are cached so that you won't have to scan all 3 spaces everytime you run the backup system.

If you want to use the cached scans in your next backup instead of re-scanning, simply set the `load_cache` member of the `backup_system` class to `True` (default is `False`).

### Snapshots
What are snapshots?

### Diff
There are 3 diff types:
1. `new` - Files that exist in `Google Drive` but don't exist in `D:/` in the same paths.
2. `modified` - Files that exist on the same paths both in `Google Drive` and in `D:/` but that their `last_modified` is different.
3. `removed` - Files that don't exist in `Google Drive` but exist in `D:/` in the same paths.

### File Types
The Backup System currently supports 3 file types:
1. Google Doc
2. Google Sheet
3. PDF

## Step-by-Step
### Google Drive Backup
When running the Backup System with the `--google-drive` flag, the backup system will:
1. Scan all 3 spaces, or load the cached scans if `load_cache` is `True`.
2. Compare the scans.
3. Download `new` and `modified` files from `Google Drive` and save them in a `./tmp` folder under their correlating paths.
4. Merge the diff into the local `D:/` drive, as follows:
   1. `new` - Moves the downloaded files from the `./tmp` folder to their destination folders.
   2. `modified` - Moves the downloaded files from the `./tmp` folder to their destination folders replacing the old files.
   3. `removed` - Deletes from the local `D:/` drive.
5. Save snapshots of the current files state for future comparisons.

### Local Backup
When running the Backup System with the `--local` flag, the backup system will:
> NOT YET IMPLEMENTED