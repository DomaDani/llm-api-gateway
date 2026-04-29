from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health", description="A simple check of the gateway status", tags=["health"])
async def health(request: Request):
    """
    Endpoint to check the health of the gateway.

    Returns
    -------
	dict
	    A simple JSON response indicating OK status and optionally the version of the gateway.
    """
    app_state = getattr(request.app, "state", None)
    version = getattr(app_state, "version", None) if app_state else None
    payload = {"status": "ok"}
    if version:
        payload["version"] = version
    return payload

# Alias for health check
@router.get("/", description="Alias for health check", tags=["health"])
async def root(request: Request):
    """
    Alias for the health check endpoint, allowing the gateway status to be checked by sending a request to the root path.

    See Also
    --------
	health
	    The main health check endpoint that this function calls to get the gateway status.
    """
    return await health(request)
