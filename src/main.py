import argparse
from backup_system import BackupSystem


def main():
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description='Backup System - What would you like to backup?')
    parser.add_argument('--local',
                        action='store_true',
                        help="Backup local files to external drive F:/")
    parser.add_argument('--google-drive',
                        action='store_true',
                        help="Backup Google Drive files to local drive D:/")

    args = parser.parse_args()
    if args.google_drive == False and args.local == False:
        print('No arguements were provided')
    else:
        backup_system = BackupSystem()
        if args.google_drive:
            backup_system.backup_google_drive_files()
        if args.local:
            backup_system.backup_local_files()


if __name__ == '__main__':
    main()
