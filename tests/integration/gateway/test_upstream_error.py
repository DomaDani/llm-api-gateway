from pathlib import Path

from tests.integration.helpers import load_mapping, post_chat_completion

def test_upstream_error(completions_url: str, unlimited_api_key: str, completions_dir: Path):
    """Verify upstream error mappings are propagated with expected status and payload."""

    mapping = load_mapping(completions_dir, "mock_completion2")
    request_data = mapping.get("request")
    expected_response = mapping.get("upstream_error", {}).get("response")
    expected_status = mapping.get("upstream_error", {}).get("status", 200)

    resp = post_chat_completion(completions_url, unlimited_api_key, request_data)
    assert resp.status_code == expected_status

    response = resp.json()
    if isinstance(expected_response, dict) and "detail" in expected_response:
        assert expected_response["detail"] in response.get("detail", "")
    else:
        assert response == expected_response