import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI(
    title="Kasi-Logistics AI Engine",
    description="Service foundation for Kasi-Logistics multi-agent routing and spatial vision",
    version="0.1.0"
)

security = HTTPBearer()
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "default-dev-token-change-me")


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Constant-time token verification to prevent timing attacks."""
    if not secrets.compare_digest(credentials.credentials, SERVICE_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing service token",
        )
    return credentials.credentials


class PingRequest(BaseModel):
    prompt: str = "Ping Kasi-Logistics Routing Engine"


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Liveness check for deployment monitoring."""
    return {"status": "ok", "service": "kasi-logistics-ai"}


@app.post("/v1/ping-model")
def ping_model(payload: PingRequest, token: str = Depends(verify_token)):
    """Test endpoint for Meta model connectivity validation."""
    return {
        "status": "success",
        "message": f"Kasi-Logistics agent received prompt: {payload.prompt}",
        "authenticated": True,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8090, reload=True)