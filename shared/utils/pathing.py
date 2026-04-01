from pathlib import Path

def find_project_root(start: Path = None, marker: str = "docker-compose.yml") -> Path:
    if start is None:
        start = Path(__file__).parent
    current = start.resolve()
    while True:
        if (current / marker).exists():
            return current
        if current.parent == current:
            raise FileNotFoundError(f"Could not find project root with {marker} starting from {start}")
        current = current.parent