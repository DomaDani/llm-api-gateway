from sqlalchemy import Row

from shared.models import UsageLog
from dashboard.backend.models import UsageLogDisplayInformation, UsageLogAggregateDisplayInformation
from dashboard.backend.db import get_project_by_id, get_user_by_id, get_key_by_id
from shared.models.orm_models import project

async def convert_orm_to_display_info(usage_log_orm: UsageLog) -> UsageLogDisplayInformation:

    if usage_log_orm.project_id is not None:
        project = await get_project_by_id(usage_log_orm.project_id)
        project_name = project.name if project else f"Project {usage_log_orm.project_id}"
    else:
        project_name = "N/A"

    if usage_log_orm.user_id is not None:
        user = await get_user_by_id(usage_log_orm.user_id)
        user_name = user.username if user else f"User {usage_log_orm.user_id}"
    else:
        user_name = "N/A"

    if usage_log_orm.key_id is not None:
        key = await get_key_by_id(usage_log_orm.key_id)
        fingerprint = key.fingerprint if key else f"Key {usage_log_orm.key_id}"
    else:
        fingerprint = "N/A"

    return UsageLogDisplayInformation(
        id=usage_log_orm.id,
        fingerprint=fingerprint,
        project_name=project_name,
        user_name=user_name,
        project_id=usage_log_orm.project_id,
        user_id=usage_log_orm.user_id,
        request_id=usage_log_orm.request_id,
        timestamp=usage_log_orm.timestamp,
        request_type=usage_log_orm.request_type,
        estimated_tokens=usage_log_orm.estimated_tokens,
        prompt_tokens=usage_log_orm.prompt_tokens,
        completion_tokens=usage_log_orm.completion_tokens,
        total_tokens=usage_log_orm.total_tokens,
        internal_cost_estimate=usage_log_orm.internal_cost_estimate,
        internal_cost_final=usage_log_orm.internal_cost_final,
        model=usage_log_orm.model,
        temperature=usage_log_orm.temperature,
        top_p=usage_log_orm.top_p,
        top_k=usage_log_orm.top_k,
        finish_reason=usage_log_orm.finish_reason,
        upstream_latency=usage_log_orm.upstream_latency,
        gateway_overhead=usage_log_orm.gateway_overhead,
        total_latency=usage_log_orm.total_latency,
        ttft=usage_log_orm.ttft,
        is_streaming=usage_log_orm.is_streaming,
        status_code=usage_log_orm.status_code,
    )


async def convert_aggregate_row_to_display_info(row: Row) -> UsageLogAggregateDisplayInformation:
    mapping = row._mapping

    if mapping["project_id"] is not None:
        project = await get_project_by_id(mapping["project_id"])
        project_name = project.name if project else f"Project {mapping['project_id']}"
    else:
        project_name = "N/A"

    if mapping["user_id"] is not None:
        user = await get_user_by_id(mapping["user_id"])
        user_name = user.username if user else f"User {mapping['user_id']}"
    else:
        user_name = "N/A"

    if mapping["key_id"] is not None:
        key = await get_key_by_id(mapping["key_id"])
        fingerprint = key.fingerprint if key else f"Key {mapping['key_id']}"
    else:
        fingerprint = "N/A"
    
    return UsageLogAggregateDisplayInformation(
        timestamp=mapping["time_chunk"],
        project_name=project_name,
        user_name=user_name,
        fingerprint=fingerprint,
        request_count=mapping["request_count"],
        total_tokens=mapping["total_tokens"],
        internal_cost_final=mapping["total_cost"],
    )
