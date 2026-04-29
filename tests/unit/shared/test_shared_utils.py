import pytest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from shared.utils import date_calc as date_mod
from shared.utils import hashing as hash_mod
from shared.utils import password as pass_mod
from shared.utils import pathing as path_mod
from shared.models.orm_models import Period
from freezegun import freeze_time


def test_hash_and_verify_key():
    """
    Test that a key hashed with hash_key can be verified with verify_key, that incorrect keys do not verify and that malformed hashes gracefully return False.
    """
    key = "secret-key-123"
    hashed = hash_mod.hash_key(key)
    assert "." in hashed
    assert hash_mod.verify_key(key, hashed) is True
    assert hash_mod.verify_key("wrong-key", hashed) is False
    assert hash_mod.verify_key(key, "not-a-valid-hash") is False



def test_password_hash_and_verify():
    """
    Tests that a password hashed with hash_password can be verified with verify_password, that incorrect passwords do not verify and that malformed hashes gracefully return False.
    """
    stored = pass_mod.hash_password("mypassword")
    assert pass_mod.verify_password(stored, "mypassword") is True
    assert pass_mod.verify_password(stored, "notmypassword") is False
    assert pass_mod.verify_password("not-a-valid-hash", "mypassword") is False


def test_find_project_root_and_missing(tmp_path):
    """
    Tests that find_project_root can correctly locate the root directory based on the marker and raises FileNotFoundError when the marker is not found.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary filesystem path provided by pytest for creating test directories and markers.
    """
    project_root = tmp_path / "projroot"
    marker_dir = project_root / "shared"
    nested_start = project_root / "src" / "pkg"
    nested_start.mkdir(parents=True)
    marker_dir.mkdir()

    found = path_mod.find_project_root(start=nested_start, marker="shared")
    assert found.resolve() == project_root.resolve()

    with pytest.raises(FileNotFoundError):
        path_mod.find_project_root(start=tmp_path / "other", marker="no-such-marker")


@pytest.mark.parametrize("period,expected_no_ff,expected_ff", [
    (Period.MINUTE, datetime(2025, 12, 12, 21, 22, 48, tzinfo=timezone.utc), datetime(2026, 4, 1, 12, 38, 48, tzinfo=timezone.utc)),
    (Period.HOUR, datetime(2025, 12, 12, 22, 21, 48, tzinfo=timezone.utc), datetime(2026, 4, 1, 13, 21, 48, tzinfo=timezone.utc)),
    (Period.DAY, datetime(2025, 12, 13, 21, 21, 48, tzinfo=timezone.utc), datetime(2026, 4, 1, 21, 21, 48, tzinfo=timezone.utc)),
    (Period.WEEK, datetime(2025, 12, 19, 21, 21, 48, tzinfo=timezone.utc), datetime(2026, 4, 3, 21, 21, 48, tzinfo=timezone.utc)),
    (Period.MONTH, datetime(2026, 1, 12, 21, 21, 48, tzinfo=timezone.utc), datetime(2026, 4, 15, 21, 21, 48, tzinfo=timezone.utc)),
])
@freeze_time("2026-04-01 12:38:03")
def test_calculate_date_after_period_behaviour(period, expected_no_ff, expected_ff):
    """Verify behaviour for both fast_forward False and True.

    Parameters
    ----------
    period : Period
        Period value under test.
    expected_no_ff : datetime
        Expected result for fast_forward=False.
    expected_ff : datetime
        Expected result for fast_forward=True.

    Returns
    -------
    None
        None.
    """
    start = datetime(2025, 12, 12, 21, 21, 48, tzinfo=timezone.utc)

    res_no_ff = date_mod.calculate_date_after_period(period, start_date=start, fast_forward=False)
    assert res_no_ff == expected_no_ff

    res_ff = date_mod.calculate_date_after_period(period, start_date=start, fast_forward=True)
    assert res_ff == expected_ff


