from shared.models import Limit
from dashboard.backend.models import LimitTypeDisplayInformation


def convert_limit_orm_to_display_info(limit_orm: Limit) -> LimitTypeDisplayInformation:
    return LimitTypeDisplayInformation(
        id=limit_orm.id,
        name=limit_orm.name,
        description=limit_orm.description,
    )
