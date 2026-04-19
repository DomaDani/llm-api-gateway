import requests
from pathlib import Path
from tests.integration.helpers import build_chat_url, load_mapping

def _build_chat_url(completions_url: str) -> str:
    """Build the chat completions URL used by this test module."""

    return build_chat_url(completions_url)


def _load_request_data(completions_dir: Path) -> dict:
    """Load the base request payload from the primary completion mapping."""

    mapping = load_mapping(completions_dir, "mock_completion1")
    return mapping.get("request")


def test_key_authentication_rejects_too_short_key(completions_url: str, completions_dir: Path):
    """Ensure malformed short API keys are rejected with a validation error."""

    request_data = _load_request_data(completions_dir)
    url = _build_chat_url(completions_url)

    headers = {"Authorization": "Bearer TooShortKey"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Invalid API Key length."


def test_key_authentication_rejects_too_long_key(completions_url: str, completions_dir: Path):
    """Ensure oversized API keys are rejected as invalid fingerprints."""

    request_data = _load_request_data(completions_dir)
    url = _build_chat_url(completions_url)

    headers = {"Authorization": "Bearer TooLongKeyTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 403
    response = resp.json()
    assert response["detail"] == "API key fingerprint invalid or not in allowed keys."


def test_key_authentication_rejects_invalid_fingerprint_with_valid_length(completions_url: str, completions_dir: Path):
    """Ensure valid-length but unknown key fingerprints are rejected."""

    request_data = _load_request_data(completions_dir)
    url = _build_chat_url(completions_url)

    headers = {"Authorization": "Bearer InvalidKeyTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 403
    response = resp.json()
    assert response["detail"] == "API key fingerprint invalid or not in allowed keys."


def test_key_authentication_rejects_expired_key(completions_url: str, expired_api_key: str, completions_dir: Path):
    """Ensure expired API keys cannot access completions."""

    request_data = _load_request_data(completions_dir)
    url = _build_chat_url(completions_url)

    headers = {"Authorization": f"Bearer {expired_api_key}"}
    resp = requests.post(url, headers=headers, json=request_data)
    assert resp.status_code == 403

    response = resp.json()
    assert response["detail"] == "The API key is not active."


def test_key_authentication_rejects_invalid_key_with_matching_fingerprint(completions_url: str, completions_dir: Path):
    """Ensure keys with matching fingerprint but invalid secret are rejected."""

    request_data = _load_request_data(completions_dir)
    url = _build_chat_url(completions_url)

    headers = {"Authorization": "Bearer TTcj1lxYOY9dInvalidWithMatchingFingerprintTTTTTTTTTTTTTTTTTTTTTT"}
    resp = requests.post(url, headers=headers, json=request_data)

    assert resp.status_code == 403
    response = resp.json()
    assert response["detail"] == "Invalid API key."
