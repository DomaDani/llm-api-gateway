from shared.models import Period
from dashboard.backend.models import PeriodDisplayInformation


def convert_period_enum_to_display_info(period: Period) -> PeriodDisplayInformation:
    return PeriodDisplayInformation(
        name=period.name,
        value=period.value,
    )
