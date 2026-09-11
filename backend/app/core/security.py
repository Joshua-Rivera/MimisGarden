"""Protect review/history data; the public prediction endpoint stays anonymous."""
import os
import secrets
import threading
import time
from collections import defaultdict, deque
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)

def require_admin(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    expected = os.getenv("ADMIN_TOKEN", "")
    if not expected:
        raise HTTPException(503, "Administration is not configured")
    if credentials is None or not secrets.compare_digest(credentials.credentials, expected):
        raise HTTPException(401, "An administrator token is required", headers={"WWW-Authenticate": "Bearer"})

_lock = threading.Lock()
_requests = defaultdict(deque)

def limit_predictions(request: Request):
    # Uses the direct peer address. Configure trusted proxy headers at deployment.
    peer = request.client.host if request.client else "unknown"
    now = time.monotonic()
    with _lock:
        for key in list(_requests):
            if not _requests[key] or _requests[key][-1] <= now - 60:
                del _requests[key]
        queue = _requests[peer]
        while queue and queue[0] <= now - 60:
            queue.popleft()
        if len(queue) >= 10:
            raise HTTPException(429, "Please wait a minute before trying again", headers={"Retry-After": "60"})
        queue.append(now)
