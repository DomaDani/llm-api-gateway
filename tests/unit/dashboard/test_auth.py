from datetime import datetime, timezone
from types import SimpleNamespace

from jose import jwt
import pytest

from dashboard.backend.auth import access_token as auth_mod
from dashboard.backend.models import AccessTokenInfo, UserDisplayInformation
from shared.config import LOGIN_SECRET_KEY, TOKEN_ENCODING_ALGORITHM


def test_create_access_token_encodes_payload():
	"""
	Verify create_access_token generates a JWT token with user data and expiration.
	"""
	token_info = AccessTokenInfo(sub="user@example.com", user_id=42)
	
	token = auth_mod.create_access_token(token_info)
	
	assert isinstance(token, str)
	assert len(token) > 0
	decoded = jwt.decode(token, LOGIN_SECRET_KEY, algorithms=[TOKEN_ENCODING_ALGORITHM])
	assert decoded["sub"] == "user@example.com"
	assert decoded["user_id"] == 42
	assert "exp" in decoded


def test_verify_access_token_valid_and_invalid():
	"""
	Verify token validation: valid tokens return True, invalid and malformed tokens return False.
	"""
	token_info = AccessTokenInfo(sub="alice@example.com", user_id=99)
	valid_token = auth_mod.create_access_token(token_info)
	
	assert auth_mod.verify_access_token(valid_token) is True
	assert auth_mod.verify_access_token("invalid-token") is False
	assert auth_mod.verify_access_token("") is False
	assert auth_mod.verify_access_token("malformed.jwt.parts") is False


@pytest.mark.asyncio
async def test_get_user_from_token_valid_invalid_missing_user(monkeypatch):
	"""
	Verify user extraction from token: valid user found returns DTO, invalid token returns None, user not found returns None.
	"""
	token_info = AccessTokenInfo(sub="bob@example.com", user_id=77)
	valid_token = auth_mod.create_access_token(token_info)
	
	async def fake_get_user_by_id(user_id):
		return None
	
	async def fake_convert_orm_to_display_info(user_orm, project_id=None):
		return UserDisplayInformation(
			id=77,
			email="bob@example.com",
			username="bob",
			joined_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
		)
	
	monkeypatch.setattr(auth_mod, "get_user_by_id", fake_get_user_by_id)
	monkeypatch.setattr(auth_mod, "convert_orm_to_display_info", fake_convert_orm_to_display_info)
	
	assert await auth_mod.get_user_from_token(valid_token) is None
	assert await auth_mod.get_user_from_token("invalid-token") is None
	assert await auth_mod.get_user_from_token("") is None


@pytest.mark.asyncio
async def test_get_user_from_token_found_user(monkeypatch):
	"""
	Verify user extraction returns DTO when token is valid and user exists in database.
	"""
	token_info = AccessTokenInfo(sub="charlie@example.com", user_id=55)
	valid_token = auth_mod.create_access_token(token_info)
	
	user_orm = SimpleNamespace(
		id=55,
		email="charlie@example.com",
		username="charlie",
		profile_picture_url=None,
		joined_date=datetime(2025, 6, 15, tzinfo=timezone.utc),
		last_login=datetime(2026, 4, 20, tzinfo=timezone.utc),
		password_expires_at=None,
	)
	
	async def fake_get_user_by_id(user_id):
		if user_id == 55:
			return user_orm
		return None
	
	async def fake_convert_orm_to_display_info(user_orm, project_id=None):
		return UserDisplayInformation(
			id=user_orm.id,
			email=user_orm.email,
			username=user_orm.username,
			profile_picture_url=user_orm.profile_picture_url,
			joined_date=user_orm.joined_date,
			last_login=user_orm.last_login,
			password_expires_at=user_orm.password_expires_at,
		)
	
	monkeypatch.setattr(auth_mod, "get_user_by_id", fake_get_user_by_id)
	monkeypatch.setattr(auth_mod, "convert_orm_to_display_info", fake_convert_orm_to_display_info)
	
	user_info = await auth_mod.get_user_from_token(valid_token)
	
	assert user_info is not None
	assert user_info.id == 55
	assert user_info.username == "charlie"
	assert user_info.email == "charlie@example.com"
