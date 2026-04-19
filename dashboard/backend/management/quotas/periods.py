from shared.models import Period
from dashboard.backend.models import PeriodDisplayInformation


def convert_period_enum_to_display_info(period: Period) -> PeriodDisplayInformation:
    """
    Convert a period enum value to a period display DTO.

    Parameters
    ----------
    - period: Period enum value.

    Returns
    -------
    - PeriodDisplayInformation with the enum name.
    """
    return PeriodDisplayInformation(
        name=period.name
    )
