from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

import dashboard.backend.db.keys as keys_mod
import dashboard.backend.db.lookups as lookups_mod
import dashboard.backend.db.permissions as perms_mod
import dashboard.backend.db.users as users_mod
from shared.models import Status
from tests.tools.mock_db import FakeResult, FakeSession


@pytest.mark.asyncio
async def test_user_availability_checks_with_and_without_exclusion(monkeypatch):
	"""
	Verify email and username availability checks for free, taken, and excluded-owner cases.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to replace `get_user_by_email` and `get_user_by_username` lookups.
	"""

	async def fake_get_user_by_email(email):
		if email == "taken@example.com":
			return SimpleNamespace(id=10)
		return None

	async def fake_get_user_by_username(username):
		if username == "taken_name":
			return SimpleNamespace(id=20)
		return None

	monkeypatch.setattr(lookups_mod, "get_user_by_email", fake_get_user_by_email)
	monkeypatch.setattr(lookups_mod, "get_user_by_username", fake_get_user_by_username)

	assert await lookups_mod.user_email_free("free@example.com") is True
	assert await lookups_mod.user_email_free("taken@example.com") is False
	assert await lookups_mod.user_email_free("taken@example.com", exclude_user_id=10) is True

	assert await lookups_mod.user_username_free("free_name") is True
	assert await lookups_mod.user_username_free("taken_name") is False
	assert await lookups_mod.user_username_free("taken_name", exclude_user_id=20) is True


@pytest.mark.asyncio
async def test_is_password_expired_returns_expected_flags():
	"""
	Verify password expiry returns true for past timestamp and false for missing or future timestamp.
	"""

	now = datetime.now(timezone.utc)
	expired_session = FakeSession([FakeResult(one=now - timedelta(days=1))])
	future_session = FakeSession([FakeResult(one=now + timedelta(days=1))])
	missing_session = FakeSession([FakeResult(one=None)])

	assert await users_mod.is_password_expired(user_id=1, session=expired_session) is True
	assert await users_mod.is_password_expired(user_id=1, session=future_session) is False
	assert await users_mod.is_password_expired(user_id=1, session=missing_session) is False


@pytest.mark.asyncio
async def test_delete_key_archives_and_missing(monkeypatch):
	"""
	Verify key deletion archives active key, removes quotas, and raises when key is missing.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to control lookup behavior for keys and quotas.
	"""

	active_quota_one = SimpleNamespace(id=101)
	active_quota_two = SimpleNamespace(id=102)
	active_key = SimpleNamespace(id=7, status=Status.ACTIVE, quotas=[active_quota_one, active_quota_two])

	success_session = FakeSession([FakeResult(rows=[active_key])])
	missing_session = FakeSession([FakeResult(rows=[])])

	await keys_mod.delete_key(key_id=7, session=success_session)

	assert active_key.status == Status.ARCHIVED
	assert success_session.deleted == [active_quota_one, active_quota_two]

	with pytest.raises(ValueError) as exc:
		await keys_mod.delete_key(key_id=999, session=missing_session)
	assert "not found" in str(exc.value).lower()


@pytest.mark.asyncio
async def test_permission_role_checks_project_scoped_and_global(monkeypatch):
	"""
	Verify member, manager, and administrator checks across scoped, global, and missing-user cases.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to replace permission and user lookup helpers.
	"""

	async def fake_get_user_permissions_for_project(project_id, user_id, session=None):
		if project_id == 11 and user_id == 1:
			return SimpleNamespace(role=SimpleNamespace(name="Project Manager"))
		if project_id == 11 and user_id == 2:
			return SimpleNamespace(role=SimpleNamespace(name="User"))
		return None

	async def fake_get_user_by_id(user_id, session=None):
		if user_id == 1:
			return SimpleNamespace(
				permissions=[
					SimpleNamespace(project=SimpleNamespace(name="Project A"), role=SimpleNamespace(name="Project Manager")),
				]
			)
		if user_id == 2:
			return SimpleNamespace(
				permissions=[
					SimpleNamespace(project=SimpleNamespace(name="Project A"), role=SimpleNamespace(name="User")),
				]
			)
		if user_id == 3:
			return SimpleNamespace(
				permissions=[
					SimpleNamespace(project=SimpleNamespace(name="Global"), role=SimpleNamespace(name="Administrator")),
				]
			)
		return None

	monkeypatch.setattr(perms_mod, "get_user_permissions_for_project", fake_get_user_permissions_for_project)
	monkeypatch.setattr(perms_mod, "get_user_by_id", fake_get_user_by_id)

	assert await perms_mod.is_user_project_member(project_id=11, user_id=1, session=SimpleNamespace()) is True
	assert await perms_mod.is_user_project_member(project_id=11, user_id=9, session=SimpleNamespace()) is False

	assert await perms_mod.is_user_project_manager(user_id=1, project_id=11, session=SimpleNamespace()) is True
	assert await perms_mod.is_user_project_manager(user_id=2, project_id=11, session=SimpleNamespace()) is False
	assert await perms_mod.is_user_project_manager(user_id=1, project_id=None, session=SimpleNamespace()) is True
	assert await perms_mod.is_user_project_manager(user_id=2, project_id=None, session=SimpleNamespace()) is False

	assert await perms_mod.is_user_administrator(user_id=3, session=SimpleNamespace()) is True
	assert await perms_mod.is_user_administrator(user_id=2, session=SimpleNamespace()) is False

	with pytest.raises(ValueError) as exc:
		await perms_mod.is_user_project_manager(user_id=999, project_id=None, session=SimpleNamespace())
	assert "not found" in str(exc.value).lower()


@pytest.mark.asyncio
async def test_delete_user_success_and_guard_rails(monkeypatch):
	"""
	Verify user deletion removes related records and blocks missing, administrator, and project-manager deletions.

	Parameters
	----------
	monkeypatch : pytest.MonkeyPatch
		Monkeypatch fixture used to replace admin/project-manager checks and delete helpers.
	"""

	user = SimpleNamespace(
		id=5,
		permissions=[SimpleNamespace(id=1), SimpleNamespace(id=2)],
		api_keys=[
			SimpleNamespace(id=11, status=Status.ACTIVE),
			SimpleNamespace(id=12, status=Status.ARCHIVED),
		],
		quotas=[SimpleNamespace(id=21), SimpleNamespace(id=22)],
	)

	delete_key_calls = []
	delete_quota_calls = []

	async def fake_is_user_administrator(user_id, session=None):
		return user_id == 6

	async def fake_is_user_project_manager(user_id, session=None):
		return user_id == 7

	async def fake_delete_key(key_id, session=None):
		delete_key_calls.append(key_id)

	async def fake_delete_quota(quota_id, session=None):
		delete_quota_calls.append(quota_id)

	monkeypatch.setattr(users_mod, "is_user_administrator", fake_is_user_administrator)
	monkeypatch.setattr(users_mod, "is_user_project_manager", fake_is_user_project_manager)
	monkeypatch.setattr(users_mod, "delete_key", fake_delete_key)
	monkeypatch.setattr(users_mod, "delete_quota", fake_delete_quota)

	success_session = FakeSession([FakeResult(rows=[user])])
	missing_session = FakeSession([FakeResult(rows=[])])
	admin_session = FakeSession([FakeResult(rows=[user])])
	manager_session = FakeSession([FakeResult(rows=[user])])

	await users_mod.delete_user(user_id=5, session=success_session)

	assert [obj.id for obj in success_session.deleted] == [1, 2, 5]
	assert delete_key_calls == [11]
	assert delete_quota_calls == [21, 22]

	with pytest.raises(ValueError) as exc:
		await users_mod.delete_user(user_id=999, session=missing_session)
	assert "not found" in str(exc.value).lower()

	with pytest.raises(ValueError) as exc:
		await users_mod.delete_user(user_id=6, session=admin_session)
	assert "administrator" in str(exc.value).lower()

	with pytest.raises(ValueError) as exc:
		await users_mod.delete_user(user_id=7, session=manager_session)
	assert "project manager" in str(exc.value).lower()
