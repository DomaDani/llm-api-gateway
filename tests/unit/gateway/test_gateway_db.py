from types import SimpleNamespace

import pytest

import gateway.db.helpers as helpers_mod
import gateway.db.keys as keys_mod
import gateway.db.limits as limits_mod
import gateway.db.refresh as refresh_mod
from shared.models import Status
from tests.tools.mock_db import FakeResult, FakeSession


@pytest.mark.asyncio
async def test_db_key_check_returns_key_and_raises_for_missing():
    """
    Verify API key lookup returns the key record when found and raises ValueError when missing.
    """

    key_record = SimpleNamespace(id=11, project_id=22, user_id=33)
    found_session = FakeSession([FakeResult(one=key_record)])
    missing_session = FakeSession([FakeResult(one=None)])

    assert await keys_mod.db_key_check("abcdefghijklmnop", session=found_session) is key_record

    with pytest.raises(ValueError):
        await keys_mod.db_key_check("abcdefghijklmnop", session=missing_session)


@pytest.mark.asyncio
async def test_get_quota_count_and_get_quotas_by_key(monkeypatch):
    """
    Verify quota counting returns the scalar count and quotas are grouped by their limit IDs.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Monkeypatch fixture used to replace module-level helpers such as `_get_limit_ids`.
    """

    async def fake_get_limit_ids(session=None):
        return 1, 2, 3

    monkeypatch.setattr(limits_mod, "_get_limit_ids", fake_get_limit_ids)

    quota_rows = [
        SimpleNamespace(id=1, limit_id=1),
        SimpleNamespace(id=2, limit_id=2),
        SimpleNamespace(id=3, limit_id=2),
        SimpleNamespace(id=4, limit_id=3),
        SimpleNamespace(id=5, limit_id=99),
    ]
    quota_session = FakeSession([FakeResult(rows=quota_rows)])
    count_session = FakeSession([FakeResult(count=7)])

    assert await helpers_mod.get_quota_count(session=count_session) == 7

    request_quotas, token_quotas, price_quotas = await limits_mod.db_get_quotas_by_key(
        SimpleNamespace(id=10, project_id=20, user_id=30),
        session=quota_session,
    )

    assert [quota.id for quota in request_quotas] == [1]
    assert [quota.id for quota in token_quotas] == [2, 3]
    assert [quota.id for quota in price_quotas] == [4]


@pytest.mark.asyncio
async def test_db_limit_change_clamps_allocations(monkeypatch):
    """
    Verify quota allocation updates clamp limited quotas and leave unlimited quotas unchanged.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Monkeypatch fixture used to replace quota retrieval helpers (e.g. `db_get_quotas_by_key`).
    """

    request_limited = SimpleNamespace(id=1, allocated=4, limit_value=5)
    request_unlimited = SimpleNamespace(id=2, allocated=10, limit_value=None)
    token_limited = SimpleNamespace(id=3, allocated=3, limit_value=8)
    price_limited = SimpleNamespace(id=4, allocated=1.5, limit_value=5)

    async def fake_db_get_quotas_by_key(api_key, session=None):
        return [request_limited, request_unlimited], [token_limited], [price_limited]

    monkeypatch.setattr(limits_mod, "db_get_quotas_by_key", fake_db_get_quotas_by_key)

    await limits_mod.db_limit_change(
        SimpleNamespace(id=99),
        request_delta=3,
        change_by_tokens=10,
        change_by_price=-2,
        session=SimpleNamespace(),
    )

    assert request_limited.allocated == 5
    assert request_unlimited.allocated == 10
    assert token_limited.allocated == 8
    assert price_limited.allocated == 0


@pytest.mark.asyncio
async def test_db_limit_check_and_allocation_handles_common_branches(monkeypatch):
    """
    Verify quota allocation succeeds with no or unlimited quotas and fails when a strict quota would be exceeded.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Monkeypatch fixture used to replace quota change and retrieval functions (`db_limit_change`, `db_get_quotas_by_key`).
    """

    change_calls = []

    async def fake_db_limit_change(api_key, request_delta=0, change_by_tokens=0, change_by_price=0, session=None):
        change_calls.append(
            {
                "api_key": api_key,
                "request_delta": request_delta,
                "change_by_tokens": change_by_tokens,
                "change_by_price": change_by_price,
                "session": session,
            }
        )

    scenarios = [
        (([], [], []), 4, 1.25, True),
        (([SimpleNamespace(allocated=1, limit_value=None)], [], []), 4, 1.25, True),
        (([SimpleNamespace(allocated=1, limit_value=1)], [], []), 4, 1.25, False),
        (([], [SimpleNamespace(allocated=2, limit_value=5)], [SimpleNamespace(allocated=1.0, limit_value=5)]), 2, 0.5, True),
    ]

    async def fake_db_get_quotas_by_key(api_key, session=None):
        (request_quotas, token_quotas, price_quotas), _, _, _ = scenarios.pop(0)
        return request_quotas, token_quotas, price_quotas

    monkeypatch.setattr(limits_mod, "db_get_quotas_by_key", fake_db_get_quotas_by_key)
    monkeypatch.setattr(limits_mod, "db_limit_change", fake_db_limit_change)

    api_key = SimpleNamespace(id=7, project_id=8, user_id=9)

    assert await limits_mod.db_limit_check_and_allocation(api_key, estimated_tokens=4, estimated_price=1.25) is True
    assert await limits_mod.db_limit_check_and_allocation(api_key, estimated_tokens=4, estimated_price=1.25) is True
    assert await limits_mod.db_limit_check_and_allocation(api_key, estimated_tokens=4, estimated_price=1.25) is False
    assert await limits_mod.db_limit_check_and_allocation(api_key, estimated_tokens=2, estimated_price=0.5) is True

    assert len(change_calls) == 1
    assert change_calls[0]["request_delta"] == 1
    assert change_calls[0]["change_by_tokens"] == 2
    assert change_calls[0]["change_by_price"] == 0.5


@pytest.mark.asyncio
async def test_refresh_and_expire_quotas_by_batch_update_rows(monkeypatch):
    """
    Verify batch refresh resets quotas and batch expiry marks active quotas as expired.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Monkeypatch fixture used to replace time advancing helpers such as `calculate_date_after_period`.
    """

    refreshed_row = SimpleNamespace(id=1, allocated=7, period="day", next_reset="old")
    expired_row = SimpleNamespace(id=2, status=Status.ACTIVE)
    refresh_session = FakeSession([
        FakeResult(),
        FakeResult(rows=[refreshed_row]),
        FakeResult(rows=[]),
    ])
    expire_session = FakeSession([
        FakeResult(),
        FakeResult(rows=[expired_row]),
        FakeResult(rows=[]),
    ])

    monkeypatch.setattr(refresh_mod, "calculate_date_after_period", lambda period, next_reset, fast_forward=False: "new")

    assert await refresh_mod.refresh_quotas_by_batch(session=refresh_session, batch_size=1) == 1
    assert refreshed_row.allocated == 0
    assert refreshed_row.next_reset == "new"

    assert await refresh_mod.expire_quotas_by_batch(session=expire_session, batch_size=1) == 1
    assert expired_row.status == Status.EXPIRED
