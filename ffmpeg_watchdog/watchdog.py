import pathlib

from decouple import config
from ffmpeg_progress_yield import FfmpegProgress
from logger import LOGGER
from rich.progress import Progress


CMD_STR = "ffmpeg -i {in_file} -c:v libx265 -crf 25 -preset slow -c:a copy " \
          "-vf crop='iw-mod(iw,2)':'ih-mod(ih,2)' -f mp4 {out_file} -hide_banner -y"
IN_FOLDER = pathlib.Path(config('IN_FOLDER'))
OUT_FOLDER = pathlib.Path(config('OUT_FOLDER'))
OUT_FOLDER.mkdir(parents=True, exist_ok=True)
EXTENSIONS = ['.webm', '.gif', '.mp4']
TARGET_EXT = '.mp4'


def replace_file(src_file: pathlib.Path, temp_file: pathlib.Path, dest_file: pathlib.Path) -> None:
    """ Сравнивает размеры, удаляет файл большего размера
    """
    temp_size = temp_file.stat().st_size
    dest_size = dest_file.stat().st_size if dest_file.is_file() else 10 ** 24

    if temp_size < dest_size:
        # если временный меньше чем существующий
        temp_file.replace(dest_file.with_suffix(TARGET_EXT))

    src_file.unlink(missing_ok=True)
    temp_file.unlink(missing_ok=True)


def process(files: list[pathlib.Path]) -> None:
    """ Обработка файлов
    """
    total_files = len(files)
    with Progress() as progress:
        file_progress = progress.add_task("[green]Processing...", total=100)
        total_progress = progress.add_task(
            "[red]Total files...", total=total_files)

        for index, file in enumerate(files, 1):
            tmp_file = OUT_FOLDER / file.with_suffix('.tmp').name
            target_file = OUT_FOLDER / file.with_suffix(TARGET_EXT).name
            print(f"[{index}/{total_files}] {file.name}")

            if file.suffix == TARGET_EXT \
                    and target_file.is_file() \
                    and target_file.stat().st_size < file.stat().st_size:
                file.unlink()
            else:
                cmd = CMD_STR.format(in_file=str(file), out_file=str(tmp_file))
                ff = FfmpegProgress(cmd.split())
                for prc in ff.run_command_with_progress():
                    progress.update(file_progress, completed=prc)
                LOGGER.info('ffmpeg stderr:\n%s', ff.stderr.strip())
                LOGGER.info('\n' + '-' * 80)
                replace_file(file, tmp_file, target_file)

            progress.update(total_progress, advance=1)


def main():
    files = [file for file in IN_FOLDER.iterdir() if file.suffix in EXTENSIONS]
    if files:
        process(files)
    else:
        print('No files! Exited')
        LOGGER.info('No files! Exited')
        exit(0)


if __name__ == '__main__':
    main()
