import os
import secrets
import time
from collections import defaultdict
from asyncio import Semaphore
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "default-dev-token-change-me")
MAX_CONCURRENT_CALLS = int(os.getenv("MAX_CONCURRENT_CALLS", "5"))
REQUESTS_PER_MINUTE_CAP = int(os.getenv("REQUESTS_PER_MINUTE_CAP", "60"))

api_semaphore = Semaphore(MAX_CONCURRENT_CALLS)
request_history = defaultdict(list)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    provided_token = credentials.credentials
    if not secrets.compare_digest(provided_token, SERVICE_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing service token",
        )
    
    now = time.time()
    timestamps = request_history[provided_token]
    request_history[provided_token] = [ts for ts in timestamps if now - ts < 60]
    
    if len(request_history[provided_token]) >= REQUESTS_PER_MINUTE_CAP:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: Credit protection limit reached for this minute.",
        )
    
    request_history[provided_token].append(now)
    return provided_token

