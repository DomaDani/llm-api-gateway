import os

import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get(
        "HEALTH_BASE_URL",
        "http://docker:8000" if (os.environ.get("CI") or os.environ.get("GITLAB_CI")) else "http://localhost:8000",
    )

@pytest.fixture(scope="session")
def unlimited_api_key() -> str:
    return os.environ.get("UNLIMITED_API_KEY", "TTcj1lxYOY9dB25bVh6IKfOrwW8ERIWHXJKqxYYwxHM-_LHTf3isqFhitJxpVGiZaLf2GVwiKsQZLhnR-xYJ2Q")

@pytest.fixture(scope="session")
def limited_api_key() -> str:
    return os.environ.get("LIMITED_API_KEY", "WQC-GPp6L8glbHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ")