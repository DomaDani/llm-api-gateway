from datetime import datetime, timedelta, timezone

from shared.models import Period

def calculate_date_after_period(period: Period, start_date: datetime | None = None, fast_forward: bool = False) -> datetime:
    """
    Calculate the next date after a given period from the start date.

    Parameters
    ----------
    - period: The period to add from the Period enum.
    - start_date: The date from which to calculate the next date. If None, the current date and time will be used.
    - fast_forward: If True, the calculation will fast-forward to the next date reachable from the start date based on the period, skipping periods that have already passed.

    Returns
    -------
    - The calculated date after the specified period.
    """
    now = datetime.now(timezone.utc)
    
    if start_date is None:
        start_date = now

    if period == Period.MINUTE:
        delta = timedelta(minutes=1)
    elif period == Period.HOUR:
        delta = timedelta(hours=1)
    elif period == Period.DAY:
        delta = timedelta(days=1)
    elif period == Period.WEEK:
        delta = timedelta(weeks=1)
    elif period == Period.MONTH:
        # Approximate a month as 31 days
        delta = timedelta(days=31)
    else:
        raise ValueError(f"Unsupported period: {period}")
    

    periods_elapsed = 0
    if fast_forward:
        time_diff = now - start_date

        periods_elapsed = (time_diff // delta) + 1

    return start_date + (periods_elapsed * delta)