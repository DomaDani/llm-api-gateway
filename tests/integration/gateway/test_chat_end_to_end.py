from pathlib import Path

from tests.integration.helpers import load_mapping, post_chat_completion

def test_chat_end_to_end(completions_url: str, unlimited_api_key: str, completions_dir: Path):
    mapping = load_mapping(completions_dir, "mock_completion1")
    request_data = mapping.get("request")
    expected_response = mapping.get("completion")

    resp = post_chat_completion(completions_url, unlimited_api_key, request_data)
    assert resp.status_code == 200

    response = resp.json()
    response["id"] = expected_response["id"]
    assert response == expected_response

