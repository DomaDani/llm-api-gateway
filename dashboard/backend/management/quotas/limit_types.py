from shared.models import Limit
from dashboard.backend.models import LimitTypeDisplayInformation


def convert_limit_orm_to_display_info(limit_orm: Limit) -> LimitTypeDisplayInformation:
    """
    Convert a limit ORM entity to a limit type display DTO.

    Parameters
    ----------
    limit_orm : Limit
        Source limit ORM model.

    Returns
    -------
    LimitTypeDisplayInformation
        LimitTypeDisplayInformation mapped from ORM data.
    """
    return LimitTypeDisplayInformation(
        id=limit_orm.id,
        name=limit_orm.name,
        description=limit_orm.description,
    )
