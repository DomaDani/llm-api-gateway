from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from gateway.auth import keys as auth_mod
from gateway.limits import quota as quota_mod
from gateway.models import OpenAIMessage, OpenAIRequest, ValidatedRequest
from shared.models import Status


@pytest.mark.asyncio
async def test_validate_api_key_accepts_valid_and_rejects_invalid_inputs(monkeypatch):
	"""
	Verify API key validation accepts a valid active key and rejects missing, short, inactive, fingerprint, and signature failures.
	"""

	monkeypatch.setattr(auth_mod, "EXPECTED_KEY_LENGTH", 8)

	valid_key = SimpleNamespace(
		id=11,
		project_id=22,
		user_id=33,
		status=Status.ACTIVE,
		key_hash="hash-abc",
	)

	async def fake_db_key_check(api_key):
		if api_key == "goodkey1":
			return valid_key
		if api_key == "inactive1":
			return SimpleNamespace(
				id=12,
				project_id=23,
				user_id=34,
				status=Status.EXPIRED,
				key_hash="hash-def",
			)
		if api_key == "badfinger":
			raise ValueError
		return valid_key

	def fake_verify_key(api_key, key_hash):
		return api_key == "goodkey1" and key_hash == "hash-abc"

	monkeypatch.setattr(auth_mod, "db_key_check", fake_db_key_check)
	monkeypatch.setattr(auth_mod, "verify_key", fake_verify_key)

	assert await auth_mod.validate_api_key(SimpleNamespace(credentials="goodkey1")) is valid_key

	with pytest.raises(HTTPException) as exc:
		await auth_mod.validate_api_key(SimpleNamespace(credentials=""))
	assert exc.value.status_code == 401
	assert exc.value.detail == "Missing API Key from headers."

	with pytest.raises(HTTPException) as exc:
		await auth_mod.validate_api_key(SimpleNamespace(credentials="short"))
	assert exc.value.status_code == 400
	assert exc.value.detail == "Invalid API Key length."

	with pytest.raises(HTTPException) as exc:
		await auth_mod.validate_api_key(SimpleNamespace(credentials="badfinger"))
	assert exc.value.status_code == 403
	assert exc.value.detail == "API key fingerprint invalid or not in allowed keys."

	with pytest.raises(HTTPException) as exc:
		await auth_mod.validate_api_key(SimpleNamespace(credentials="inactive1"))
	assert exc.value.status_code == 403
	assert exc.value.detail == "The API key is not active."

	with pytest.raises(HTTPException) as exc:
		await auth_mod.validate_api_key(SimpleNamespace(credentials="wrongkey"))
	assert exc.value.status_code == 403
	assert exc.value.detail == "Invalid API key."


@pytest.mark.asyncio
async def test_check_limits_costs_returns_validated_request_and_blocks_over_quota(monkeypatch):
	"""
	Verify quota checking returns a validated request when allocation succeeds and raises 429 when allocation fails.
	"""

	monkeypatch.setattr(quota_mod, "QUOTA_STRICTNESS", 0.5)
	monkeypatch.setattr(quota_mod, "DEFAULT_MAX_COMPLETION_TOKENS", 20)

	captured = {}

	def fake_get_token_count(messages):
		captured["messages"] = messages
		return 12

	def fake_calculate_cost(*, usage, model_ref, provider_id):
		captured["usage"] = usage
		captured["model_ref"] = model_ref
		captured["provider_id"] = provider_id
		return 4.5

	allocation_results = [True, False]

	async def fake_db_limit_check_and_allocation(key_info, estimated_total_tokens, estimated_cost):
		captured.setdefault("allocations", []).append(
			{
				"key_info": key_info,
				"estimated_total_tokens": estimated_total_tokens,
				"estimated_cost": estimated_cost,
			}
		)
		return allocation_results.pop(0)

	monkeypatch.setattr(quota_mod, "get_token_count", fake_get_token_count)
	monkeypatch.setattr(quota_mod, "calculate_cost", fake_calculate_cost)
	monkeypatch.setattr(quota_mod, "db_limit_check_and_allocation", fake_db_limit_check_and_allocation)

	body = OpenAIRequest(
		model="test-model",
		messages=[OpenAIMessage(role="user", content="Hello")],
		max_completion_tokens=10,
	)
	key_info = SimpleNamespace(id=7, project_id=8, user_id=9)

	result = await quota_mod.check_limits_costs(body, key_info)

	assert isinstance(result, ValidatedRequest)
	assert result.key_id == 7
	assert result.project_id == 8
	assert result.user_id == 9
	assert result.body is body
	assert result.estimated_tokens == 17
	assert result.internal_cost_estimate == 4.5
	assert captured["messages"] == body.messages
	assert captured["usage"].input_tokens == 12
	assert captured["usage"].output_tokens == 5
	assert captured["model_ref"] == "test-model"

	with pytest.raises(HTTPException) as exc:
		await quota_mod.check_limits_costs(body, key_info)
	assert exc.value.status_code == 429
	assert exc.value.detail == "Quota exceeded."
