import pytest
from fastapi.testclient import TestClient

from gateway.app.factory import create_app as create_gateway_app
from dashboard.backend.app.factory import create_app as create_dashboard_app
from gateway.models import OpenAIMessage, OpenAIRequest, ValidatedRequest


@pytest.fixture(scope="module")
def gateway_client():
    """
    Return a TestClient instance for unit testing the gateway.
    """
    app = create_gateway_app()
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def dashboard_client():
    """
    Return a TestClient instance for unit testing the dashboard.
    """
    app = create_dashboard_app()
    with TestClient(app) as c:
        yield c

@pytest.fixture
def validated_request():
    """Return a minimal validated request object for gateway utility tests."""
    return ValidatedRequest(
        key_id=11,
        project_id=22,
        user_id=33,
        body=OpenAIRequest(
            model="test-model",
            messages=[OpenAIMessage(role="user", content="hello")],
            stream=True,
        ),
        estimated_tokens=44,
        internal_cost_estimate=0.12,
    )
