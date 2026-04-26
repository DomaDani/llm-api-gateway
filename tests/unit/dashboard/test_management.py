from types import SimpleNamespace

from fastapi import HTTPException
import pytest

from dashboard.backend.management.users import passwords as pwd_mod
from dashboard.backend.management.quotas import permissions as quota_perms_mod
from dashboard.backend.management.quotas import creation as quota_creation_mod
from dashboard.backend.management.keys import permissions as key_perms_mod


@pytest.mark.asyncio
async def test_enforce_password_strength_valid_and_invalid(monkeypatch):
    """
    Verify strong passwords pass, weak passwords raise with appropriate detail.
    """
    assert await pwd_mod.enforce_password_strength("ValidPass1") is None
    
    with pytest.raises(HTTPException) as exc:
        await pwd_mod.enforce_password_strength("short1A")
    assert exc.value.status_code == 400
    assert "8 characters" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await pwd_mod.enforce_password_strength("nouppercase1")
    assert exc.value.status_code == 400
    assert "uppercase" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await pwd_mod.enforce_password_strength("NOLOWERCASE1")
    assert exc.value.status_code == 400
    assert "lowercase" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await pwd_mod.enforce_password_strength("NoDigitsHere")
    assert exc.value.status_code == 400
    assert "digit" in exc.value.detail


@pytest.mark.asyncio
async def test_enforce_password_change_validity_scenarios(monkeypatch):
    """
    Verify password change: correct current, strength check, no reuse, confirmation match.
    """
    def fake_verify_password(stored_hash, provided_password):
        return provided_password == "CurrentCorrect1"
    
    monkeypatch.setattr(pwd_mod, "verify_password", fake_verify_password)
    
    with pytest.raises(HTTPException) as exc:
        await pwd_mod.enforce_password_change_validity("wrong-password", "hash-abc", "NewPass1", "NewPass1")
    assert exc.value.status_code == 400
    assert "incorrect" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await pwd_mod.enforce_password_change_validity("CurrentCorrect1", "hash-abc", "CurrentCorrect1", "CurrentCorrect1")
    assert exc.value.status_code == 400
    assert "different" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await pwd_mod.enforce_password_change_validity("CurrentCorrect1", "hash-abc", "NewPass1", "Different1")
    assert exc.value.status_code == 400
    assert "not match" in exc.value.detail
    
    await pwd_mod.enforce_password_change_validity("CurrentCorrect1", "hash-abc", "NewValid1", "NewValid1")


@pytest.mark.asyncio
async def test_enforce_quota_creation_permission_scenarios(monkeypatch):
    """
    Verify quota creation: admin for global, project manager for scoped, non-admin denied.
    """
    async def fake_is_user_administrator(user_id):
        return user_id == 1
    
    async def fake_is_user_project_manager(user_id, project_id):
        return user_id == 2 and project_id == 10
    
    monkeypatch.setattr(quota_perms_mod, "is_user_administrator", fake_is_user_administrator)
    monkeypatch.setattr(quota_perms_mod, "is_user_project_manager", fake_is_user_project_manager)
    
    assert await quota_perms_mod.enforce_quota_creation_permission(1, None, None, None) is None
    assert await quota_perms_mod.enforce_quota_creation_permission(2, 10, None, None) is None
    
    with pytest.raises(HTTPException) as exc:
        await quota_perms_mod.enforce_quota_creation_permission(3, None, None, None)
    assert exc.value.status_code == 403
    assert "Administrator" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await quota_perms_mod.enforce_quota_creation_permission(3, 10, None, None)
    assert exc.value.status_code == 403
    assert "Project manager" in exc.value.detail


@pytest.mark.asyncio
async def test_enforce_quota_deletion_permission_scenarios(monkeypatch):
    """
    Verify quota deletion: admin unrestricted, project manager for their project, others denied.
    """
    async def fake_is_user_administrator(user_id):
        return user_id == 1
    
    async def fake_get_quota_by_id(quota_id):
        if quota_id == 100:
            return SimpleNamespace(
                id=100,
                project_id=5,
                api_key=None,
            )
        elif quota_id == 200:
            return SimpleNamespace(
                id=200,
                project_id=None,
                api_key=None,
            )
        return None
    
    async def fake_is_user_project_manager(user_id, project_id):
        return user_id == 2 and project_id == 5
    
    monkeypatch.setattr(quota_perms_mod, "is_user_administrator", fake_is_user_administrator)
    monkeypatch.setattr(quota_perms_mod, "get_quota_by_id", fake_get_quota_by_id)
    monkeypatch.setattr(quota_perms_mod, "is_user_project_manager", fake_is_user_project_manager)
    
    assert await quota_perms_mod.enforce_quota_deletion_permission(1, 100) is None
    assert await quota_perms_mod.enforce_quota_deletion_permission(2, 100) is None
    
    with pytest.raises(HTTPException) as exc:
        await quota_perms_mod.enforce_quota_deletion_permission(3, 100)
    assert exc.value.status_code == 403
    assert "Project manager" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await quota_perms_mod.enforce_quota_deletion_permission(3, 200)
    assert exc.value.status_code == 403
    assert "administrators" in exc.value.detail


@pytest.mark.asyncio
async def test_enforce_existing_limit_found_and_not_found(monkeypatch):
    """
    Verify limit check passes when exists, raises 404 when not.
    """
    async def fake_get_limit_by_id(limit_id):
        if limit_id == 1:
            return SimpleNamespace(id=1, name="Tokens")
        return None
    
    monkeypatch.setattr(quota_creation_mod, "get_limit_by_id", fake_get_limit_by_id)
    
    assert await quota_creation_mod.enforce_existing_limit(1) is None
    
    with pytest.raises(HTTPException) as exc:
        await quota_creation_mod.enforce_existing_limit(999)
    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail


@pytest.mark.asyncio
async def test_enforce_existing_quota_target_scenarios(monkeypatch):
    """
    Verify quota target check validates all present entities, raises 404 for missing.
    """
    async def fake_get_project_by_id(project_id):
        return SimpleNamespace(id=5) if project_id == 5 else None
    
    async def fake_get_user_by_id(user_id):
        return SimpleNamespace(id=10) if user_id == 10 else None
    
    async def fake_get_key_by_id(key_id):
        return SimpleNamespace(id=20) if key_id == 20 else None
    
    monkeypatch.setattr(quota_creation_mod, "get_project_by_id", fake_get_project_by_id)
    monkeypatch.setattr(quota_creation_mod, "get_user_by_id", fake_get_user_by_id)
    monkeypatch.setattr(quota_creation_mod, "get_key_by_id", fake_get_key_by_id)
    
    assert await quota_creation_mod.enforce_existing_quota_target(5, 10, 20) is None
    assert await quota_creation_mod.enforce_existing_quota_target(None, None, None) is None
    
    with pytest.raises(HTTPException) as exc:
        await quota_creation_mod.enforce_existing_quota_target(999, None, None)
    assert exc.value.status_code == 404
    assert "Project" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await quota_creation_mod.enforce_existing_quota_target(None, 999, None)
    assert exc.value.status_code == 404
    assert "User" in exc.value.detail
    
    with pytest.raises(HTTPException) as exc:
        await quota_creation_mod.enforce_existing_quota_target(None, None, 999)
    assert exc.value.status_code == 404
    assert "API key" in exc.value.detail


@pytest.mark.asyncio
async def test_enforce_key_deletion_permission_scenarios(monkeypatch):
    """
    Verify key deletion: admin unrestricted, owner or project manager allowed, others denied.
    """
    async def fake_is_user_administrator(user_id):
        return user_id == 1
    
    async def fake_get_key_ownership(key_id):
        if key_id == 100:
            return (
                SimpleNamespace(id=5),
                SimpleNamespace(id=2),
            )
        return (None, None)
    
    async def fake_is_user_project_manager(user_id, project_id):
        return user_id == 3 and project_id == 5
    
    monkeypatch.setattr(key_perms_mod, "is_user_administrator", fake_is_user_administrator)
    monkeypatch.setattr(key_perms_mod, "get_key_ownership", fake_get_key_ownership)
    monkeypatch.setattr(key_perms_mod, "is_user_project_manager", fake_is_user_project_manager)
    
    assert await key_perms_mod.enforce_key_deletion_permission(1, 100) is None
    assert await key_perms_mod.enforce_key_deletion_permission(2, 100) is None
    assert await key_perms_mod.enforce_key_deletion_permission(3, 100) is None
    
    with pytest.raises(HTTPException) as exc:
        await key_perms_mod.enforce_key_deletion_permission(4, 100)
    assert exc.value.status_code == 403
    assert "own API keys" in exc.value.detail
