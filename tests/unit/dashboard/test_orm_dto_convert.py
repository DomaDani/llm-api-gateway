from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace

import pytest

from shared.models import Period, Status
from dashboard.backend.management.keys import information as key_info_mod
from dashboard.backend.management.projects import information as project_info_mod
from dashboard.backend.management.quotas import information as quota_info_mod
from dashboard.backend.management.quotas import limit_types as limit_types_mod
from dashboard.backend.management.quotas import periods as periods_mod
from dashboard.backend.management.users import identities as user_identities_mod
from dashboard.backend.management.usage_logs import information as usage_logs_mod


def test_convert_key_orm_to_display_info_with_related_username():
	"""
	Verify key ORM to DTO conversion uses related user username when no override is provided.
	"""
	created_at = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
	key_orm = SimpleNamespace(
		id=10,
		project_id=20,
		user_id=30,
		user=SimpleNamespace(username="alice"),
		name="Primary",
		fingerprint="fp-123",
		create_date=created_at,
		status=Status.ACTIVE,
	)

	dto = key_info_mod.convert_orm_to_display_info(key_orm)

	assert dto.id == 10
	assert dto.project_id == 20
	assert dto.user_id == 30
	assert dto.username == "alice"
	assert dto.name == "Primary"
	assert dto.fingerprint == "fp-123"
	assert dto.api_key is None
	assert dto.create_date == created_at
	assert dto.status == Status.ACTIVE


def test_convert_key_orm_to_display_info_with_overrides():
	"""
	Verify key ORM to DTO conversion prefers explicit username and api_key overrides.
	"""
	key_orm = SimpleNamespace(
		id=11,
		project_id=21,
		user_id=31,
		user=SimpleNamespace(username="ignored"),
		name="Secondary",
		fingerprint="fp-999",
		create_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
		status=Status.BLOCKED,
	)

	dto = key_info_mod.convert_orm_to_display_info(
		key_orm,
		api_key="sk-test-123",
		username="override-user",
	)

	assert dto.username == "override-user"
	assert dto.api_key == "sk-test-123"


def test_convert_project_orm_to_display_info():
	"""
	Verify project ORM to DTO conversion maps identity, name, status and timestamps.
	"""
	created_at = datetime(2025, 10, 5, 6, 7, 8, tzinfo=timezone.utc)
	modified_at = datetime(2025, 10, 6, 7, 8, 9, tzinfo=timezone.utc)
	project_orm = SimpleNamespace(
		id=7,
		name="Alpha",
		status=Status.ACTIVE,
		created_date=created_at,
		modified_date=modified_at,
	)

	dto = project_info_mod.convert_orm_to_display_info(project_orm)

	assert dto.id == 7
	assert dto.name == "Alpha"
	assert dto.status == Status.ACTIVE
	assert dto.created_date == created_at
	assert dto.modified_date == modified_at


@pytest.mark.asyncio
async def test_convert_quota_orm_to_display_info_with_name(monkeypatch):
	"""
	Verify quota ORM to DTO conversion maps fields and generated name with lookups.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to replace lookup helpers (`get_limit_by_id`, `get_user_by_id`, `get_key_by_id`).
	"""
	now = datetime(2026, 4, 24, 12, 0, 0, tzinfo=timezone.utc)
	quota_orm = SimpleNamespace(
		id=5,
		project_id=9,
		user_id=13,
		key_id=17,
		project=SimpleNamespace(name="Project-X"),
		user=SimpleNamespace(username="bob"),
		api_key=SimpleNamespace(name="ServiceKey"),
		limit_id=3,
		limit_value=2500.0,
		period="day",
		expires_at=now,
		status=Status.ACTIVE,
		allocated=500.0,
		next_reset=now,
	)

	async def fake_get_limit_by_id(limit_id):
		return SimpleNamespace(name="Tokens")

	async def fake_get_user_by_id(user_id):
		return SimpleNamespace(username="bob")

	async def fake_get_key_by_id(key_id):
		return SimpleNamespace(fingerprint="fp-abc")

	monkeypatch.setattr(quota_info_mod, "get_limit_by_id", fake_get_limit_by_id)
	monkeypatch.setattr(quota_info_mod, "get_user_by_id", fake_get_user_by_id)
	monkeypatch.setattr(quota_info_mod, "get_key_by_id", fake_get_key_by_id)

	dto = await quota_info_mod.convert_orm_to_display_info(quota_orm, add_name=True)

	assert dto.id == 5
	assert dto.name == "Project-X User-Specific [bob] Key-Specific [ServiceKey] Tokens"
	assert dto.project_id == 9
	assert dto.user_name == "bob"
	assert dto.fingerprint == "fp-abc"
	assert dto.limit_id == 3
	assert dto.limit_name == "Tokens"
	assert dto.limit_value == 2500.0
	assert dto.period == "day"
	assert dto.expires_at == now
	assert dto.status == Status.ACTIVE
	assert dto.allocated == 500.0
	assert dto.next_reset == now


def test_convert_limit_orm_to_display_info():
	"""
	Verify limit ORM to DTO conversion maps id, name and description.
	"""
	limit_orm = SimpleNamespace(id=1, name="Request Limit", description="Limits the number of requests that can be made within a certain period.")

	dto = limit_types_mod.convert_limit_orm_to_display_info(limit_orm)

	assert dto.id == 1
	assert dto.name == "Request Limit"
	assert dto.description == "Limits the number of requests that can be made within a certain period."


def test_convert_period_enum_to_display_info():
	"""
	Verify period enum to DTO conversion exposes the enum name.
	"""
	dto = periods_mod.convert_period_enum_to_display_info(Period.WEEK)

	assert dto.name == "WEEK"


@pytest.mark.asyncio
async def test_convert_user_orm_to_display_info_with_role(monkeypatch):
	"""
	Verify user ORM to DTO conversion maps fields and resolved role flags.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to replace role/permission helper functions (`is_user_administrator`, `is_user_project_manager`, etc.).
	"""
	joined_at = datetime(2026, 2, 1, 10, 0, 0, tzinfo=timezone.utc)
	login_at = datetime(2026, 2, 2, 10, 0, 0, tzinfo=timezone.utc)
	expires_at = datetime(2026, 3, 1, 10, 0, 0, tzinfo=timezone.utc)
	user_orm = SimpleNamespace(
		id=101,
		email="dev@example.com",
		username="devuser",
		profile_picture_url="https://example.com/p.png",
		joined_date=joined_at,
		last_login=login_at,
		password_expires_at=expires_at,
	)

	async def fake_is_user_administrator(user_id):
		return True

	async def fake_is_user_project_manager(user_id, project_id=None):
		return True

	async def fake_is_password_expired(user_id):
		return False

	async def fake_get_user_permissions_for_project(project_id, user_id):
		return SimpleNamespace(role=SimpleNamespace(name="Editor"))

	monkeypatch.setattr(user_identities_mod, "is_user_administrator", fake_is_user_administrator)
	monkeypatch.setattr(user_identities_mod, "is_user_project_manager", fake_is_user_project_manager)
	monkeypatch.setattr(user_identities_mod, "is_password_expired", fake_is_password_expired)
	monkeypatch.setattr(user_identities_mod, "get_user_permissions_for_project", fake_get_user_permissions_for_project)

	dto = await user_identities_mod.convert_orm_to_display_info(
		user_orm,
		include_role=True,
		project_id=7,
	)

	assert dto.id == 101
	assert str(dto.email) == "dev@example.com"
	assert dto.username == "devuser"
	assert dto.profile_picture_url == "https://example.com/p.png"
	assert dto.joined_date == joined_at
	assert dto.last_login == login_at
	assert dto.password_expires_at == expires_at
	assert dto.role == "Editor"
	assert dto.is_admin is True
	assert dto.is_project_manager is True
	assert dto.is_password_expired is False


@pytest.mark.asyncio
async def test_convert_usage_log_orm_to_display_info(monkeypatch):
	"""
	Verify usage log ORM to DTO conversion maps values and resolved display names.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to replace project/user/key lookup helpers used when resolving names.
	"""
	now = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
	usage_log_orm = SimpleNamespace(
		id=1,
		key_id=77,
		project_id=55,
		user_id=66,
		request_id="req-1",
		timestamp=now,
		request_type="chat.completion",
		estimated_tokens=100,
		prompt_tokens=40,
		completion_tokens=60,
		total_tokens=100,
		internal_cost_estimate=Decimal("0.010"),
		internal_cost_final=Decimal("0.012"),
		model="gpt-test",
		temperature=0.3,
		top_p=0.8,
		top_k=20,
		finish_reason="stop",
		upstream_latency=0.7,
		gateway_overhead=0.05,
		total_latency=0.75,
		ttft=0.1,
		is_streaming=False,
		status_code=200,
	)

	async def fake_get_project_by_id(project_id):
		return SimpleNamespace(name="Project-A")

	async def fake_get_user_by_id(user_id):
		return SimpleNamespace(username="sam")

	async def fake_get_key_by_id(key_id):
		return SimpleNamespace(fingerprint="fp-777")

	monkeypatch.setattr(usage_logs_mod, "get_project_by_id", fake_get_project_by_id)
	monkeypatch.setattr(usage_logs_mod, "get_user_by_id", fake_get_user_by_id)
	monkeypatch.setattr(usage_logs_mod, "get_key_by_id", fake_get_key_by_id)

	dto = await usage_logs_mod.convert_orm_to_display_info(usage_log_orm)

	assert dto.id == 1
	assert dto.fingerprint == "fp-777"
	assert dto.project_name == "Project-A"
	assert dto.user_name == "sam"
	assert dto.request_id == "req-1"
	assert dto.timestamp == now
	assert dto.total_tokens == 100
	assert dto.internal_cost_final == Decimal("0.012")


@pytest.mark.asyncio
async def test_convert_aggregate_row_to_display_info(monkeypatch):
	"""
	Verify aggregate row to DTO conversion maps row values and resolved display names.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to replace project/user/key lookup helpers used when resolving names.
	"""
	now = datetime(2026, 4, 2, 0, 0, 0, tzinfo=timezone.utc)
	row = SimpleNamespace(
		_mapping={
			"time_chunk": now,
			"project_id": 10,
			"user_id": 20,
			"key_id": 30,
			"request_count": 9,
			"total_tokens": 1234,
			"total_cost": Decimal("1.234"),
		}
	)

	async def fake_get_project_by_id(project_id):
		return SimpleNamespace(name="Project-Z")

	async def fake_get_user_by_id(user_id):
		return SimpleNamespace(username="ivy")

	async def fake_get_key_by_id(key_id):
		return SimpleNamespace(fingerprint="fp-30")

	monkeypatch.setattr(usage_logs_mod, "get_project_by_id", fake_get_project_by_id)
	monkeypatch.setattr(usage_logs_mod, "get_user_by_id", fake_get_user_by_id)
	monkeypatch.setattr(usage_logs_mod, "get_key_by_id", fake_get_key_by_id)

	dto = await usage_logs_mod.convert_aggregate_row_to_display_info(row)

	assert dto.timestamp == now
	assert dto.project_name == "Project-Z"
	assert dto.user_name == "ivy"
	assert dto.fingerprint == "fp-30"
	assert dto.request_count == 9
	assert dto.total_tokens == 1234
	assert dto.internal_cost_final == Decimal("1.234")

