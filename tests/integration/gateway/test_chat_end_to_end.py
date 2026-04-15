from tests.tools.load_mappings import load_mappings_from_dir
import requests
from pathlib import Path

def test_chat_end_to_end(completions_url: str, unlimited_api_key: str, completions_dir: Path):
    mappings = load_mappings_from_dir(completions_dir, "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")
    expected_response = mappings.get("mock_completion1", {}).get("completion")

    url = f"{completions_url}/chat/completions"
    headers = {"Authorization": f"Bearer {unlimited_api_key}"}
    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == 200

    response = resp.json()
    response["id"] = expected_response["id"]
    assert response == expected_response

