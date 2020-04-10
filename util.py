# v0.0.1 utilities
def event_folders(path) -> set:
    """
    Creates a set of event folders under the input path.
    The set contains all the folders as Path.

    :param path:  root path
    :type path: str or Path
    :rtype: set (Path)
    """
    from pathlib import Path
    import re
    root = path if isinstance(path, Path) else Path(str(path))
    if not root.exists():
        raise FileNotFoundError(str(root) + ' does not exist.')
    if not root.is_dir():
        raise NotADirectoryError(str(root) + ' is not a directory.')
    return set(event for event in root.glob('[0-9]*[A-Z]') if re.search('\\d+[A-Z]', str(event)))
