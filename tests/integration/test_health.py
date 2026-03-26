import requests
import time

def _wait_for_health(url: str, timeout: int = 30, interval: float = 1.0) -> requests.Response:
	end = time.time() + timeout
	while time.time() < end:
		try:
			resp = requests.get(url, timeout=5)
			if resp.status_code == 200:
				return resp
		except requests.RequestException:
			pass
		time.sleep(interval)
	raise AssertionError(f"Timed out waiting for {url}")

def test_health_endpoint_returns_200(base_url: str):
	# Integration test: the gateway /health returns 200.
	resp = _wait_for_health(f"{base_url}/health")
	assert resp.status_code == 200
	data = resp.json()
	assert data.get("status") == "ok"
