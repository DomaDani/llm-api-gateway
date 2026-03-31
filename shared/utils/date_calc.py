from datetime import datetime, timedelta, timezone

from shared.models.orm_models import Period

def calculate_date_after_period(period: Period, start_date: datetime = datetime.now(timezone.utc)) -> datetime:
    if period == Period.MINUTE:
        return start_date + timedelta(minutes=1)
    elif period == Period.HOUR:
        return start_date + timedelta(hours=1)
    elif period == Period.DAY:
        return start_date + timedelta(days=1)
    elif period == Period.WEEK:
        return start_date + timedelta(weeks=1)
    elif period == Period.MONTH:
        # Approximate a month as 31 days
        return start_date + timedelta(days=31)
    else:
        raise ValueError(f"Unsupported period: {period}")