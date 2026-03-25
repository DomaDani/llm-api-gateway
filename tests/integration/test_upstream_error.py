from tools.load_mappings import load_mappings_from_dir
from openai import OpenAI

def test_upstream_error(base_url: str, unlimited_api_key: str):
    mappings = load_mappings_from_dir("tests/fixtures/llm_responses/completions", "mock_completion2")
    request_data = mappings.get("mock_completion2", {}).get("request")
    expected_response = mappings.get("mock_completion2", {}).get("upstream_error", {}).get("response")
    expected_status_code = mappings.get("mock_completion2", {}).get("upstream_error", {}).get("status_code", 200)

    client = OpenAI(api_key=unlimited_api_key, base_url=base_url)
    
    chat_completion = client.chat.completions.create(**request_data)
    assert chat_completion.status_code == expected_status_code

    response = chat_completion.model_dump()
    assert response == expected_response