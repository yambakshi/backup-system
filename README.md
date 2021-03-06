# Backup System
Backup system for backing up Google Drive files and local files

## Setup
1.  Open cmd

2.  Navigate to projects folder
    > cd "Python Projects"

2.  Create project folder
    > mkdir "Backup System"

3.  Clone repo to project folder
    > git clone https://github.com/yambakshi/backup-system.git .

4.  Create project virtual environment:
    > python -m venv env

5.  Open vscode in project folder
    > code .

6.  In vscode create 'src' folder in the project directory

7.  Create 'main.py' in 'src' folder
    This should make vscode's python extension recognize 'env' virtualenv and set its interpertor to the venv's interperter

8.  In order to activate the venv in vscode's terminal you first need to enable running powershell scripts
    First check what's the current policy by running
    > get-executionpolicy

    The output should be 'Restricted' which is the default policy that's preventing you from running the venv activation script that's located in:
    > env/Scripts/Activate.ps1

    To change the execution policy run:
    > Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

    Then activate venv by running:
    > env/Scripts/Activate.ps1

## Requirements
Updating requirements.txt with currently installed pip packages (-l or --local flag to save only local packages and not global):
> pip freeze -l > requirements.txt

To install requirements.txt packages:
> pip install -r requirements.txt