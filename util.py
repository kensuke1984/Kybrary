# v0.0.3 utilities
from pathlib import Path


def m0_to_mw(m0: float):
    from math import log10
    return round((log10(m0) - 9.1) / 1.5, 1)


def event_folders(path) -> set:
    """
    Creates a set of event folders under the input path.
    The set contains all the folders as Path.

    :param path:  root path
    :type path: str or Path
    :rtype: set (Path)
    """
    import re
    root = path if isinstance(path, Path) else Path(str(path))
    if not root.exists():
        raise FileNotFoundError(str(root) + ' does not exist.')
    if not root.is_dir():
        raise NotADirectoryError(str(root) + ' is not a directory.')
    return set(event for event in root.glob('[0-9]*[A-Z]')
               if re.search('\\d+[A-Z]', str(event)))


class SACFileName:

    def __init__(self, path: Path):
        self.__path = path
        self.name = path.name
        parts = path.name.split('.')
        self.station = parts[0]
        self.event_id = parts[1]
        self.extension = parts[-1]

    def get_path(self):
        return self.__path

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
