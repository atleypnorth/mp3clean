import argparse
import logging
from pathlib import Path
from tinytag import TinyTag


_logger = logging.getLogger('mp3Clean')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('music_base_dir', help='top level directory of where music goes')
    parser.add_argument('--start_dir', help='where to start scanning from, default is music_base_dir')
    args = parser.parse_args()
    if args.start_dir is None:
        args.start_dir = args.music_base_dir
    return args


def get_wanted(base_dir, mp3_file):
    tag = TinyTag.get(str(mp3_file))
    if tag.title is None:
        # stick with current name ...
        file_name = mp3_file.name
    else:
        if tag.track is not None:
            file_name = '%02d_%s.mp3' % (int(tag.track), tag.title)
        else:
            file_name = '%s.mp3' % (tag.title)
    if tag.artist is not None and tag.album is not None:
        directory = Path(base_dir, Path(tag.artist), Path(tag.album))
    else:
        directory = mp3_file.parent
    return (directory, file_name)


def scan_dir(base_dir, path):
    _logger.debug('Searching %s', path)
    for mp3 in path.iterdir():
        if mp3.name.endswith('.mp3'):
            _logger.debug('Found %s', mp3)
            (directory, file_name) = get_wanted(base_dir, mp3)
            expected_path = Path(directory, Path(file_name))
            if expected_path == mp3:
                _logger.info(expected_path)
                # _logger.info('Has correct directory and path!')
            else:
                _logger.warning('Got %s', mp3)
                _logger.warning('Wanted %s', expected_path)
        elif mp3.is_dir():
            scan_dir(base_dir, mp3)


def main():
    args = get_arguments()
    scan_dir(Path(args.music_base_dir), Path(args.start_dir))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.WARNING)
    main()