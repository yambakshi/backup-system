import argparse
from backup_system import BackupSystem


def main():
    parser = argparse.ArgumentParser(description='Backup system')

    backup_system = BackupSystem()
    backup_system.backup_google_drive_files()


if __name__ == '__main__':
    main()
