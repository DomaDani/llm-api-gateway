from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health", description="A simple check of the gateway status", tags=["health"])
async def health(request: Request):
    app_state = getattr(request.app, "state", None)
    version = getattr(app_state, "version", None) if app_state else None
    payload = {"status": "ok"}
    if version:
        payload["version"] = version
    return payload

# Alias for health check
@router.get("/", description="Alias for health check", tags=["health"])
async def root(request: Request):
    return await health(request)
