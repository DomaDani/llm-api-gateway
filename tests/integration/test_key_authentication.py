import requests
from pathlib import Path
from tests.tools.load_mappings import load_mappings_from_dir

def test_key_authentication(completions_url: str, expired_api_key: str, completions_dir: Path):
    mappings = load_mappings_from_dir(completions_dir, "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")

    # Test with an API key that is too short
    url = f"{completions_url}/chat/completions"
    headers = {"Authorization": "Bearer TooShortKey"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Invalid API Key length."

    # Test with an API key that is too long (this is allowed and only fail due to the invalid fingerprint)
    headers = {"Authorization": "Bearer TooLongKeyTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 401
    response = resp.json()
    assert response["detail"] == "API key fingerprint invalid or not in allowed keys."

    # Test with an API key that has a valid length but invalid fingerprint
    headers = {"Authorization": "Bearer InvalidKeyTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 401
    response = resp.json()
    assert response["detail"] == "API key fingerprint invalid or not in allowed keys."

    # Test with an API key that is valid but expired
    headers = {"Authorization": f"Bearer {expired_api_key}"}
    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == 403

    response = resp.json()
    assert response["detail"] == "The API key is not active."

    # Test with an API key that has a valid length and fingerprint but is invalid
    headers = {"Authorization": "Bearer TTcj1lxYOY9dInvalidWithMatchingFingerprintTTTTTTTTTTTTTTTTTTTTTT"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 401
    response = resp.json()
    assert response["detail"] == "Invalid API key."
