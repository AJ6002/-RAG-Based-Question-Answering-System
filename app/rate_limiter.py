import time
from fastapi import Request, HTTPException

RATE_LIMIT = 10        # requests
TIME_WINDOW = 60       # seconds

request_log = {}

def rate_limiter(request: Request):
    ip = request.client.host
    now = time.time()

    if ip not in request_log:
        request_log[ip] = []

    # Remove old timestamps
    request_log[ip] = [
        t for t in request_log[ip]
        if now - t < TIME_WINDOW
    ]

    if len(request_log[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    request_log[ip].append(now)
