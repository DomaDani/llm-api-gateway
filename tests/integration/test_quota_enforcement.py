from tests.tools.load_mappings import load_mappings_from_dir
import requests
from pathlib import Path

def test_quota_enforcement(completions_url: str, limited_api_key: str, completions_dir: Path):
    mappings = load_mappings_from_dir(completions_dir, "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")
    expected_response = mappings.get("mock_completion1", {}).get("completion")

    url = f"{completions_url}/chat/completions"
    headers = {"Authorization": f"Bearer {limited_api_key}"}

    # Test with a request that immediately exceeds the quota
    body = {
        "model": request_data["model"],
        "messages": request_data["messages"],
        "temperature": request_data["temperature"],
        "max_tokens": 5000,
    }
    resp = requests.post(url, headers=headers, json=body)

    assert resp.status_code == 429
    response = resp.json()
    assert response["detail"] == "Quota exceeded."

    # Test with a request that is within the quota
    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == 200

    response = resp.json()
    assert response == expected_response

    # Test with another request that now exceeds the quota
    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == 429
    response = resp.json()
    assert response["detail"] == "Quota exceeded."