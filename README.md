# Backup System
Backup system for `Google Drive` and local files.

## Technologies
- Python 3.9.0

## Setup
### 1. Virtual Environment
Open `VSCode` from the repo's root, open the terminal, and create a virtual environment named `env`:
```
python -m venv env
```
**Windows 10**
1. Check the current execution policy (in order to activate the virtual environment in `VSCode`'s terminal you'll first need to enable running powershell scripts):
   ```
   get-executionpolicy
   ```
2. The default execution policy, `Restricted`, is preventing you from running the virtual environment's activation script that's in:
   ```
   env/Scripts/Activate.ps1
   ```
3. Set the execution policy for the current user to `RemoteSigned`:
   ```
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. Activate the virtual environment:
   ```
   env/Scripts/Activate.ps1
   ```
**Usefull Commands**
- Deactivate the virtual environment:
   ```
   deactivate
   ```

### 2. PIP Packages
1. Before installing the `pip` packages, make sure that the `env` virtual environment is activated (notice the `(env)` in the beginning):
   ```
   (env) PS D:\Yam Bakshi\Careers\Hi-Tech\Portfolio\Python\Backup System >
   ```
2. Install `pip` packages:
   ```
   pip install -r requirements.txt
   ```
   
**Windows 10**
- `pip` packages folders:
   - Virtual Environment - `<repo_root>\env\Lib\site-packages`
   - Global - `C:\Program Files\Python39\Lib\site-packages`

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
Set the virtual environment's interperter in `VSCode`:
1. Hit `Ctrl`+`Shift`+`P`.
2. Type `Python: Select Interpreter` and hit `Enter` to edit the setting.
3. Select `Python 3.9.0 ('env':venv) .\env\Scripts\python.exe`.

## Run
```
python ./src/main.py --google-drive
# or
python ./src/main.py --local
```

## Knowledge Base
### Flags
There are 2 flags you can pass to the Backup System:
- `--google-drive` - Backup `Google Drive` files to local drive `D:/`
- `--local` - Backup local files to external drive `F:/`

### Spaces
There are 3 spaces:
- **local** - `D:/`
- **drive_stream** - `G:/`
- **drive** - `Google Drive`

### Caches
Scans are cached so you won't have to scan all 3 spaces everytime you run the backup system.

Each line in the cache file is a list of metadata values separated by `|` of a single scanned file:
- **file_path**
- **last_modified**
- **id** (`drive` cache only - each `Google Drive` file has a unique ID)
- **is_google_type** (`drive` cache only - `gsheet` and `gdoc` are google types but `pdf` is not)

### Diff
There are 3 diff types:
- `new` - Files that exist in `Google Drive` but don't exist in `D:/` in the same paths.
- `modified` - Files that exist on the same paths both in `Google Drive` and in `D:/` but that their `last_modified` is different.
- `removed` - Files that don't exist in `Google Drive` but exist in `D:/` in the same paths.

> NOTE: If you move a file to a different folder or rename it, it will be marked as a `new` file and the original file path or file name will be marked as `removed`.

### File Types
The Backup System currently supports 3 file types:
- **Google Doc**
- **Google Sheet**
- **PDF**

### Data Structure
The `scan_results` data structure:
- **space** (e.g. `drive_stream`, `local`, `drive`)
   - **file_type** (e.g. `Google Doc`, `Google Sheet`, `PDF`)
      - **file_path** (e.g. _Car\Licenses\2020-2021.pdf_)
         - **last_modified**: _number_
         - **id**: _string_ (`drive` only - each `Google Drive` file has a unique ID)
         - **is_google_type**: _boolean_ (`drive` only - `gsheet` and `gdoc` are google types but `pdf` is not)

### Delete Microsoft Office Temp Files
1. Open `cmd` and `cd` to temp file folder.
2. List hidden files:
   ```
   dir /a:h .
   ```
3. Delete hidden file:
   ```
   del /a:h "~$rtoons - Lyrics.docx"
   ```

### Google Drive Backup
When running the Backup System with the `--google-drive` flag, the backup system will:

**1. Scan**

Scan all 3 spaces, or load the cached scans if cache files exist.

**2. Compare**

Compare `drive` scan to `local` scan.

**3. Download**

Download `new` and `modified` Google Type files only from `Google Drive` and save them in a `./tmp` folder under their correlating paths (the reason for only downloading Google type files is that any other file type is copied directly from `Google Drive` stream `G:/`)

**4. Merge**

Merge the diff into the local `D:/` drive, as follows:
   - `new` - Moves the downloaded files from the `./tmp` folder to their destination folders.
   - `modified` - Moves the downloaded files from the `./tmp` folder to their destination folders replacing the old files.
   - `removed` - Deletes from the local `D:/` drive.

**5. Cleanup**

Delete `tmp` folder

### Local Backup
When running the Backup System with the `--local` flag, the backup system will:
> NOT YET IMPLEMENTED