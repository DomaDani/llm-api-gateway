#!/usr/bin/env python3
from sqlalchemy import select

from argon2 import PasswordHasher
from datetime import datetime, timezone

import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.models import *
from shared.utils import hash_key, calculate_date_after_period

from shared.db import get_transactional_session

ph = PasswordHasher()

import asyncio


async def create_mock_data(default_only: bool = False):
    async with get_transactional_session() as session:
        
        existing_roles_result = await session.execute(select(Role))        
        role_map = {role.name: role for role in existing_roles_result.scalars().all()}

        existing_limits_result = await session.execute(select(Limit))
        limit_map = {limit.name: limit for limit in existing_limits_result.scalars().all()}

        existing_limits_result = await session.execute(select(Limit.name))
        existing_limit_names = set(existing_limits_result.scalars().all())

        if "Project Manager" not in role_map:
            pm_role = Role(
                name="Project Manager",
                description="Manages the project, sets quotas and permissions."
            )
            session.add(pm_role)
        else:
            pm_role = role_map["Project Manager"]


        if "User" not in role_map:
            user_role = Role(
                name="User",
                description="Has access to the project and can make API calls within the assigned quotas."
            )
            session.add(user_role)
        else:
            user_role = role_map["User"]


        if "Request Limit" not in limit_map:
            request_limit = Limit(
                name="Request Limit",
                description="Limits the number of requests that can be made within a certain period.",
            )
            session.add(request_limit)
        else:
            request_limit = limit_map["Request Limit"]


        if "Token Limit" not in limit_map:
            token_limit = Limit(
                name="Token Limit",
                description="Limits the number of tokens that can be used within a certain period.",
            )
            session.add(token_limit)
        else:
            token_limit = limit_map["Token Limit"]

        if default_only:
            return

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

        project_permission1 = ProjectPermission(
            project=project,
            user=user1,
            role=pm_role,
            join_date=datetime.now(timezone.utc)
        )

        project_permission2 = ProjectPermission(
            project=project,
            user=user2,
            role=user_role,
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
            name="Token Limited API key",
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

        api_key4 = APIKey(
            project=project,
            user=user2,
            name="Request Limited API key",
            fingerprint="xGn6E7jl5ocd",
            key_hash=hash_key("xGn6E7jl5ocdBNti1jZ3lQGIkznOzGgkTDsK48ng-B4f0HcNnmiChC295AWjlArwtcRICNDNukmT0Z1YFpR7-w"),
            create_date=datetime.now(timezone.utc),
            status=Status.ACTIVE
        )

        session.add_all([api_key1, api_key2, api_key3, api_key4])

        quota1 = Quota(
            api_key=api_key2,
            limit=token_limit,
            limit_value=1000,
            period=Period.HOUR,
            status=Status.ACTIVE,
            next_reset=calculate_date_after_period(Period.HOUR)
        )

        quota2 = Quota(
            api_key=api_key4,
            limit=request_limit,
            limit_value=50,
            period=Period.DAY,
            status=Status.ACTIVE,
            next_reset=calculate_date_after_period(Period.DAY)
        )

        session.add_all([quota1, quota2])


if __name__ == "__main__":
    asyncio.run(create_mock_data())