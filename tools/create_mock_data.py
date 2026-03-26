#!/usr/bin/env python3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timezone

import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.models import *
from shared.utils import hash_key

from shared.db import get_transactional_session

ph = PasswordHasher()

import asyncio


async def create_mock_data():
    async with get_transactional_session() as session:
        
        user1 = User(
            email="gipsz.jakab@teshervaals.com",
            username="GipszJakab38",
            password_hash=ph.hash("Ikarus280T"),
            joined_date=datetime.now(timezone.utc)
        )

        user2 = User(
            email="janos.a.hegyrol@domadani.hu",
            username="JonAHegyrol",
            password_hash=ph.hash("kisebbmintharomu"),
            joined_date=datetime.now(timezone.utc)
        )

        session.add_all([user1, user2])

        project = Project(
            name="Test Project",
            status=Status.ACTIVE,
            created_date=datetime.now(timezone.utc)
        )

        session.add(project)

        role1 = Role(
            name="Project Manager",
            description="Manages the project, sets quotas and permissions."
        )
        role2 = Role(
            name="User",
            description="Has access to the project and can make API calls within the assigned quotas."
        )

        session.add_all([role1, role2])

        project_permission1 = ProjectPermission(
            project=project,
            user=user1,
            role=role1,
            join_date=datetime.now(timezone.utc)
        )

        project_permission2 = ProjectPermission(
            project=project,
            user=user2,
            role=role2,
            join_date=datetime.now(timezone.utc)
        )

        session.add_all([project_permission1, project_permission2])

        api_key1 = APIKey(
            project=project,
            user=user2,
            name="End to end API key",
            fingerprint="TTcj1lxYOY9d",
            key_hash=hash_key("TTcj1lxYOY9dB25bVh6IKfOrwW8ERIWHXJKqxYYwxHM-_LHTf3isqFhitJxpVGiZaLf2GVwiKsQZLhnR-xYJ2Q"),
            create_date=datetime.now(timezone.utc),
            status=Status.ACTIVE
        )

        api_key2 = APIKey(
            project=project,
            user=user2,
            name="Limited API key",
            fingerprint="WQC-GPp6L8gl",
            key_hash=hash_key("WQC-GPp6L8glbHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ"),
            create_date=datetime.now(timezone.utc),
            status=Status.ACTIVE
        )

        api_key3 = APIKey(
            project=project,
            user=user2,
            name="Expired API key",
            fingerprint="ExpiredKey12",
            key_hash=hash_key("ExpiredKey123bHgIqAmyTQjwwr6mOV3Ar3uuWG33x0j_HzGsD-7DxujaCl-EzkTkQwZBWSekQwvtnw-WNUKnDQ"),
            create_date=datetime.now(timezone.utc),
            status=Status.EXPIRED
        )

        session.add_all([api_key1, api_key2, api_key3])

        limit = Limit(
            name="Token Limit",
            description="Limits the number of tokens that can be used within a certain period.",
        )

        session.add(limit)

        quota = Quota(
            api_key=api_key2,
            limit=limit,
            limit_value=1000,
            period=Period.HOUR,
            status=Status.ACTIVE
        )

        session.add(quota)


if __name__ == "__main__":
    asyncio.run(create_mock_data())