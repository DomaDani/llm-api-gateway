from tools.load_mappings import load_mappings_from_dir
from openai import OpenAI

def test_quota_enforcement(base_url: str, limited_api_key: str):
    mappings = load_mappings_from_dir("tests/fixtures/llm_responses/completions", "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")
    expected_response = mappings.get("mock_completion1", {}).get("completion")

    client = OpenAI(api_key=limited_api_key, base_url=base_url)

    chat_completion = client.chat.completions.create(
        model=request_data["model"],
        messages=request_data["messages"],
        temperature=request_data["temperature"],
        max_tokens=5000
    )

    assert chat_completion.status_code == 429
    response = chat_completion.model_dump()
    assert response["detail"] == "Quota exceeded."

    chat_completion = client.chat.completions.create(**request_data)
    assert chat_completion.status_code == 200

    response = chat_completion.model_dump()
    assert response == expected_response

    chat_completion = client.chat.completions.create(**request_data)
    assert chat_completion.status_code == 429
    response = chat_completion.model_dump()
    assert response["detail"] == "Quota exceeded."