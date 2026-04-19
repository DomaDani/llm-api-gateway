from tests.integration.helpers import wait_for_health

def test_health_endpoint_returns_200(base_url: str):
	"""Verify the gateway health endpoint reports an operational status."""

	resp = wait_for_health(f"{base_url}/health")
	assert resp.status_code == 200
	data = resp.json()
	assert data.get("status") == "ok"
