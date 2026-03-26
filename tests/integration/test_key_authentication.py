from openai import OpenAI, base_url
from pathlib import Path
from tests.tools.load_mappings import load_mappings_from_dir

def test_key_authentication(completions_url: str, expired_api_key: str, completions_dir: Path):
    mappings = load_mappings_from_dir(completions_dir, "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")

    # Test with an API key that is too short
    clinet = OpenAI(api_key="TooShortKey", base_url=completions_url, max_retries=0)
    chat_completion = clinet.chat.completions.create(**request_data)

    assert chat_completion.status == 400
    response = chat_completion.model_dump()
    assert response["detail"] == "Invalid API Key length."

    # Test with an API key that is too long
    client = OpenAI(api_key="TooLongKeyTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT", base_url=completions_url, max_retries=0)
    chat_completion = client.chat.completions.create(**request_data)

    assert chat_completion.status == 400
    response = chat_completion.model_dump()
    assert response["detail"] == "Invalid API Key length."

    # Test with an API key that has a valid length but invalid fingerprint
    client = OpenAI(api_key="InvalidKeyTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT", base_url=completions_url, max_retries=0)
    chat_completion = client.chat.completions.create(**request_data)

    assert chat_completion.status == 401
    response = chat_completion.model_dump()
    assert response["detail"] == "API key fingerprint invalid or not in allowed keys."

    # Test with an API key that is valid but expired
    client = OpenAI(api_key=expired_api_key, base_url=completions_url, max_retries=0)
    chat_completion = client.chat.completions.create(**request_data)
    assert chat_completion.status == 403

    response = chat_completion.model_dump()
    assert response["detail"] == "The API key is not active."

    # Test with an API key that has a valid length and fingerprint but is invalid
    client = OpenAI(api_key="TTcj1lxYOY9dInvalidWithMatchingFingerprintTTTTTTTTTTTTTTTTTTTTTT", base_url=completions_url, max_retries=0)
    chat_completion = client.chat.completions.create(**request_data)

    assert chat_completion.status == 401
    response = chat_completion.model_dump()
    assert response["detail"] == "Invalid API key."
