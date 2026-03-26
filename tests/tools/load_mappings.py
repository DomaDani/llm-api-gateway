from pathlib import Path
import json

def load_mappings_from_dir(directory: str|Path, file: str = None) -> dict:
    mappings = {}
    if isinstance(directory, str):
        directory = Path(directory)

    if not directory.is_absolute():
        directory = (Path.cwd() / directory).resolve()


    if not directory.exists():
        return
    if file:
        p = directory / file
        if p.is_file() and p.suffix.lower() == ".json":
            with p.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            mappings[p.stem] = data
            return mappings
    for p in sorted(directory.iterdir()):
        if p.is_file() and p.suffix.lower() == ".json":
            with p.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            mappings[p.stem] = data

    return mappings