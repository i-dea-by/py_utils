#!/mnt/zfs_pool/zfs_dataset/scripts/clean_recycle/venv/bin/pyton3.9
import pathlib
from datetime import datetime

from decouple import config
from loguru import logger

CLEAN_AFTER_DAYS = config('CLEAN_AFTER_DAYS', cast=int)
CLEAN_PATH = pathlib.Path(config('CLEAN_PATH'))

BASE_DIR = pathlib.Path(__file__).parent
logger.add(BASE_DIR / 'cleaner.log')

NOW = datetime.now()

def last_access_days(file: pathlib.Path) -> datetime:
    """ Return last access in days
    """
    access_time = datetime.fromtimestamp(file.stat().st_atime)
    delta = NOW - access_time
    return delta.days


def last_change_days(file: pathlib.Path) -> datetime:
    """ Return last change in days
    """
    access_time = datetime.fromtimestamp(file.stat().st_mtime)
    delta = NOW - access_time
    return delta.days


def main():
    all_files = [file for file in CLEAN_PATH.glob('**/*') if file.is_file()]
    logger.info(f"Cleanup interval: {CLEAN_AFTER_DAYS} days. Total {len(all_files):_} files.")
    to_delete = [file for file in all_files if last_access_days(file) > CLEAN_AFTER_DAYS]
    logger.info(f"Found {len(to_delete):_} files to delete.")
    if to_delete:
        for item in to_delete:
            logger.info(f"[DELETE]:{item}")
            item.unlink(missing_ok=True)
    else:
        logger.info('No files')


if __name__ == '__main__':
    logger.info('Start')
    main()
    logger.info('Stop')
