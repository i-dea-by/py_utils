#!/mnt/zfs_pool/zfs_dataset/scripts/clean_recycle/venv/pyton
import pathlib
from datetime import datetime
from loguru import logger

# root = pathlib.Path('/mnt/zfs_pool/zfs_dataset/Volume_1/.recycle')
root = pathlib.Path(r'd:\temp')
files = [file for file in root.glob('**/*') if file.is_file()]
now = datetime.now()
DAYS = 90


def last_access_days(file: pathlib.Path):
    access_time = datetime.fromtimestamp(file.stat().st_atime)
    delta = now - access_time
    return delta.days


def last_change_days(file: pathlib.Path):
    access_time = datetime.fromtimestamp(file.stat().st_mtime)
    delta = now - access_time
    return delta.days


def main():
    to_delete = [file for file in files if last_access_days(file) > DAYS]
    for item in to_delete:
        print(f"{item.name} - {last_access_days(item)}")


if __name__ == '__main__':
    main()
