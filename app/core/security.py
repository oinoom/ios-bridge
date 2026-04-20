from __future__ import annotations

import secrets
from typing import Optional

from fastapi import HTTPException, Request, WebSocket, status
from fastapi.responses import JSONResponse

from app.config.settings import settings


EXEMPT_HTTP_PATHS = {
    "/health",
}


def auth_enabled() -> bool:
    return bool(settings.ACCESS_TOKEN)


def file_bridge_enabled() -> bool:
    return settings.ENABLE_FILE_BRIDGE


def debug_routes_enabled() -> bool:
    return settings.ENABLE_DEBUG_ROUTES


def is_loopback_host(host: str) -> bool:
    normalized = (host or "").strip().lower()
    return normalized in {"127.0.0.1", "::1", "localhost"}


def is_exempt_http_path(path: str) -> bool:
    return path in EXEMPT_HTTP_PATHS


def _normalized_token(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _matches_expected_token(candidate: Optional[str]) -> bool:
    expected = settings.ACCESS_TOKEN
    candidate = _normalized_token(candidate)
    if not expected:
        return True
    if not candidate:
        return False
    return secrets.compare_digest(candidate, expected)


def extract_request_token(request: Request) -> Optional[str]:
    authorization = request.headers.get("authorization", "")
    if authorization.lower().startswith("bearer "):
        return _normalized_token(authorization.split(" ", 1)[1])

    header_token = _normalized_token(request.headers.get(settings.AUTH_HEADER_NAME))
    if header_token:
        return header_token

    query_token = _normalized_token(request.query_params.get("token"))
    if query_token:
        return query_token

    return _normalized_token(request.cookies.get(settings.AUTH_COOKIE_NAME))


def extract_websocket_token(websocket: WebSocket) -> Optional[str]:
    authorization = websocket.headers.get("authorization", "")
    if authorization.lower().startswith("bearer "):
        return _normalized_token(authorization.split(" ", 1)[1])

    header_token = _normalized_token(websocket.headers.get(settings.AUTH_HEADER_NAME))
    if header_token:
        return header_token

    query_token = _normalized_token(websocket.query_params.get("token"))
    if query_token:
        return query_token

    return _normalized_token(websocket.cookies.get(settings.AUTH_COOKIE_NAME))


def request_is_authorized(request: Request) -> bool:
    return _matches_expected_token(extract_request_token(request))


def websocket_is_authorized(websocket: WebSocket) -> bool:
    return _matches_expected_token(extract_websocket_token(websocket))


def unauthorized_response() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "success": False,
            "error": "Authentication required. Provide the shared token via query, cookie, or X-IOS-Bridge-Token header.",
        },
    )


def set_auth_cookie_if_needed(response, token: Optional[str]) -> None:
    normalized = _normalized_token(token)
    if not normalized or not auth_enabled():
        return

    response.set_cookie(
        settings.AUTH_COOKIE_NAME,
        normalized,
        httponly=True,
        samesite="lax",
        max_age=8 * 60 * 60,
    )


def ensure_file_bridge_enabled() -> None:
    if file_bridge_enabled():
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="File bridge endpoints are disabled by default in this hardened fork. Set IOS_BRIDGE_ENABLE_FILE_BRIDGE=1 to re-enable them.",
    )
