import logging
from fastapi import FastAPI, Depends, File, UploadFile, status, HTTPException

from app.security import verify_token, api_semaphore
from app.agent.spatial import SAM31SpatialSegmenter, SegmentationResult
from app.agent.optimizer import (
    RouteOptimizationRequest,
    OptimizedRouteResponse,
    KasiRouteOptimizer,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kasi-Logistics AI Engine",
    description="Spatial route optimization and wholesale pooling engine with SAM 3.1 & PayMerch Mobile escrow.",
    version="1.0.0",
)

# Initialize SAM 3.1 Spatial Vision Pipeline
segmenter = SAM31SpatialSegmenter()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Public health check endpoint (no auth required)."""
    return {"status": "healthy", "service": "kasi-logistics-ai"}


@app.get("/v1/ping-model", status_code=status.HTTP_200_OK)
async def ping_model(token: str = Depends(verify_token)):
    """Authenticated ping endpoint to verify gateway and security token validity."""
    return {
        "status": "connected",
        "active_models": ["SAM 3.1", "Muse Spark Open"],
        "message": "Gateway successfully authenticated and operational.",
    }


@app.post("/v1/spatial/segment", response_model=SegmentationResult, status_code=status.HTTP_200_OK)
async def segment_spatial_imagery(
    file: UploadFile = File(...),
    token: str = Depends(verify_token),
):
    """
    Upload aerial or ground camera imagery of informal township layouts 
    for SAM 3.1 spatial segmentation into traversable navigation nodes.
    Protected by bearer token validation, rate limiting, and concurrency semaphores.
    """
    async with api_semaphore:
        try:
            image_bytes = await file.read()
            if not image_bytes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Uploaded file is empty.",
                )
            
            result = segmenter.segment_alleyway(
                image_bytes=image_bytes,
                image_id=file.filename or "uploaded_frame_001",
            )
            return result
        except Exception as e:
            logger.error(f"Spatial segmentation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Segmentation processing error: {str(e)}",
            )


@app.post("/v1/routes/optimize", response_model=OptimizedRouteResponse, status_code=status.HTTP_200_OK)
async def optimize_delivery_route(
    payload: RouteOptimizationRequest,
    token: str = Depends(verify_token),
):
    """
    Optimizes multi-stop delivery routes for wholesale micro-merchants
    across informal township layouts using capacity-constrained routing.
    Protected by bearer token authentication and concurrency limits.
    """
    async with api_semaphore:
        try:
            result = KasiRouteOptimizer.optimize_route(payload)
            return result
        except Exception as e:
            logger.error(f"Route optimization failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Route optimization error: {str(e)}",
            )