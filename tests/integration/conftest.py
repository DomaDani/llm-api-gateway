import os

import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get(
        "HEALTH_BASE_URL",
        "http://docker:8000" if (os.environ.get("CI") or os.environ.get("GITLAB_CI")) else "http://localhost:8000",
    )
