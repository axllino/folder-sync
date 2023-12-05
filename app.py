import shutil
import argparse
import time
from pathlib import Path


def synchronize_folders(source, replica, log_file):
    source_path = Path(source)
    replica_path = Path(replica)

    # Ensures that the replica folder exists; if not, create
    replica_path.mkdir(parents=True, exist_ok=True)

    # Cycle through the files in the source folder
    for source_file in source_path.glob('*'):
        replica_file = replica_path / source_file.name

        # If the file already exists in the replica folder, check if it needs to be updated
        if replica_file.exists() and source_file.stat().st_mtime > replica_file.stat().st_mtime:
            shutil.copy2(source_file, replica_file)
            log_operation('Update', source_file, log_file)
        # If the file does not exist in the replica folder, make the copy
        elif not replica_file.exists():
            shutil.copy2(source_file, replica_file)
            log_operation('Creation', source_file, log_file)

    # Checks the replica folder for files that no longer exist in the source folder
    for replica_file in replica_path.glob('*'):
        source_file = source_path / replica_file.name

        # If the file no longer exists in the source folder, remove it from the replica folder
        if not source_file.exists():
            replica_file.unlink()
            log_operation('Removal', replica_file, log_file)


def log_operation(operation, file, log_file):
    with open(log_file, 'a') as file_log:
        file_log.write(f'{operation}: {file}\n')
    print(f'{operation}: {file}')


def main():
    parser = argparse.ArgumentParser(
        description='Program to synchronize two folders.')
    parser.add_argument('source', help='Path of the source folder')
    parser.add_argument('replica', help='Path of the replica folder')
    parser.add_argument('log_file', help='Path of the log file')
    parser.add_argument('--interval', type=int, default=60,
                        help='Synchronization interval in seconds')

    args = parser.parse_args()

    while True:
        synchronize_folders(args.source, args.replica, args.log_file)
        time.sleep(args.interval)


if __name__ == '__main__':  # the paths must be inserted
    main(synchronize_folders('original folder path',
         'replica folder path', 'log file'))
