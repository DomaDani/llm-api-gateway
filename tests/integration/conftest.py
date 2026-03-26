import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get(
        "BASE_URL",
        "http://docker:8000" if (os.environ.get("CI") or os.environ.get("GITLAB_CI")) else "http://localhost:8000",
    )

@pytest.fixture(scope="session")
def completions_url(base_url: str) -> str:
    return f"{base_url}/v1"

@pytest.fixture(scope="session")
def unlimited_api_key() -> str:
    return os.environ.get("UNLIMITED_API_KEY", "TTcj1lxYOY9dB25bVh6IKfOrwW8ERIWHXJKqxYYwxHM-_LHTf3isqFhitJxpVGiZaLf2GVwiKsQZLhnR-xYJ2Q")

@pytest.fixture(scope="session")
def limited_api_key() -> str:
    return os.environ.get("LIMITED_API_KEY", "WQC-GPp6L8glbHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ")

@pytest.fixture(scope="session")
def expired_api_key() -> str:
    return os.environ.get("EXPIRED_API_KEY", "ExpiredKey123bHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ")

@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).parents[1] / "fixtures"

@pytest.fixture(scope="session")
def completions_dir(fixtures_dir: Path) -> Path:
    return fixtures_dir  / "completions"