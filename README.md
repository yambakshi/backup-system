# Backup System
Backup system for backing up Google Drive files and local files.
This project was generated with:
- Python version: 3.9.0

## Setup
1. Open `cmd` and navigate to the projects folder:
```
cd "Python Projects"
```

2. Create project folder:
```
mkdir "Backup System"
```

3. Clone repo into project folder:
```
git clone https://github.com/yambakshi/backup-system.git .
```

4. Create project virtual environment:
```
python -m venv env
```

5. Open vscode in project folder:
```
code .
```

6. In vscode create `src` folder in the project directory:
```
mkdir src
```

7. Create `main.py` in `src` folder in order for vscode's python extension to recognize the `env` virtualenv and set its interpertor to the venv's interperter:
```
touch main.py
```

8. In order to activate the `venv` in vscode's terminal you first need to enable running powershell scripts.
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

## Requirements
Updating `requirements.txt` with currently installed pip packages (-l or --local flag to save only local packages and not global):
```
pip freeze -l > requirements.txt
```

To install `requirements.txt` packages:
```
pip install -r requirements.txt
```