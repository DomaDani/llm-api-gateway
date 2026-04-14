from datetime import datetime, timedelta, timezone

from shared.models.orm_models import Period

def calculate_date_after_period(period: Period, start_date: datetime | None = None, fast_forward: bool = False) -> datetime:
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