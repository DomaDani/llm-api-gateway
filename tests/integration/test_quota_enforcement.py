from tests.tools.load_mappings import load_mappings_from_dir
from openai import OpenAI
from pathlib import Path

def test_quota_enforcement(completions_url: str, limited_api_key: str, completions_dir: Path):
    mappings = load_mappings_from_dir(completions_dir, "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")
    expected_response = mappings.get("mock_completion1", {}).get("completion")

    client = OpenAI(api_key=limited_api_key, base_url=completions_url)


    # Test with a request that immediately exceeds the quota
    chat_completion = client.chat.completions.create(
        model=request_data["model"],
        messages=request_data["messages"],
        temperature=request_data["temperature"],
        max_tokens=5000
    )

    assert chat_completion.status_code == 429
    response = chat_completion.model_dump()
    assert response["detail"] == "Quota exceeded."

    # Test with a request that is within the quota
    chat_completion = client.chat.completions.create(**request_data)
    assert chat_completion.status_code == 200

    response = chat_completion.model_dump()
    assert response == expected_response

    # Test with another request that now exceeds the quota
    chat_completion = client.chat.completions.create(**request_data)
    assert chat_completion.status_code == 429
    response = chat_completion.model_dump()
    assert response["detail"] == "Quota exceeded."