from pathlib import Path

def find_project_root(start: Path = None, marker: str = "shared/") -> Path:
    """
    Tries to find the project root directory by looking for a specific marker file or directory (default is "shared/") starting from the given path and moving up the directory tree until it finds the marker or reaches the filesystem root.
    Used to locate the project root directory inside Docker containers where folder structures may differ.

    Parameters
    ----------
    - start: The starting path to begin the search. If None, it defaults to the directory of this file.
    - marker: The name of the file or directory to look for as an indicator of the project root. Defaults to "shared/".

    Returns
    -------
    - Path: The path to the project root directory.
    """
    if start is None:
        start = Path(__file__).parent
    current = start.resolve()
    while True:
        if (current / marker).exists():
            return current
        if current.parent == current:
            raise FileNotFoundError(f"Could not find project root with {marker} starting from {start}")
        current = current.parent