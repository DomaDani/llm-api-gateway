from tests.tools.load_mappings import load_mappings_from_dir
from openai import OpenAI
from pathlib import Path

def test_chat_end_to_end(completions_url: str, unlimited_api_key: str, completions_dir: Path):
    mappings = load_mappings_from_dir(completions_dir, "mock_completion1")
    request_data = mappings.get("mock_completion1", {}).get("request")
    expected_response = mappings.get("mock_completion1", {}).get("completion")

    client = OpenAI(api_key=unlimited_api_key, base_url=completions_url, max_retries=0)

    chat_completion = client.chat.completions.create(**request_data)
    assert chat_completion.status_code == 200

    response = chat_completion.model_dump()
    assert response == expected_response

