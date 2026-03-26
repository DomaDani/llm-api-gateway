from tests.tools.load_mappings import load_mappings_from_dir
import requests
from pathlib import Path

def test_upstream_error(completions_url: str, unlimited_api_key: str, completions_dir: Path):
    mappings = load_mappings_from_dir(completions_dir, "mock_completion2")
    request_data = mappings.get("mock_completion2", {}).get("request")
    expected_response = mappings.get("mock_completion2", {}).get("upstream_error", {}).get("response")
    expected_status = mappings.get("mock_completion2", {}).get("upstream_error", {}).get("status", 200)

    url = f"{completions_url}/chat/completions"
    headers = {"Authorization": f"Bearer {unlimited_api_key}"}

    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == expected_status

    response = resp.json()
    if isinstance(expected_response, dict) and "detail" in expected_response:
        assert expected_response["detail"] in response.get("detail", "")
    else:
        assert response == expected_response