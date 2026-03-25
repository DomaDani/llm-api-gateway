import requests
from tools.load_mappings import load_mappings_from_dir
from openai import OpenAI

def test_chat_end_to_end(base_url: str, unlimited_api_key: str):
    mappings = load_mappings_from_dir("tests/fixtures/llm_responses/completions", "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")
    expected_response = mappings.get("mock_completion1", {}).get("completion")

    client = OpenAI(api_key=unlimited_api_key, base_url=base_url)
    chat_completion = client.chat.completions.create(**request_data)

    response = chat_completion.model_dump()
    assert response == expected_response

