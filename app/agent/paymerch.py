from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

router = APIRouter(prefix="/v1/paymerch", tags=["PayMerch Mobile Fintech"])

class WalletInitRequest(BaseModel):
    merchant_id: str
    merchant_name: str
    phone_number: str
    initial_balance_zar: float = 0.0

class EscrowCreateRequest(BaseModel):
    order_id: str
    merchant_id: str
    wholesaler_id: str
    amount_zar: float
    items_summary: List[str]

class EscrowReleaseRequest(BaseModel):
    escrow_id: str
    confirmation_code: str
    delivery_verified: bool

# In-memory storage optimized for hackathon speed & reliability
WALLETS_DB = {}
ESCROWS_DB = {}

@router.post("/wallet/initialize")
def initialize_wallet(payload: WalletInitRequest):
    """Initialize a closed-loop digital wallet for an informal marketplace merchant."""
    wallet_id = f"wal_{uuid.uuid4().hex[:8]}"
    WALLETS_DB[payload.merchant_id] = {
        "wallet_id": wallet_id,
        **payload.dict(),
        "status": "active"
    }
    return {
        "status": "success", 
        "wallet_id": wallet_id, 
        "message": f"Digital wallet initialized for {payload.merchant_name}",
        "data": WALLETS_DB[payload.merchant_id]
    }

@router.post("/escrow/create")
def create_escrow(payload: EscrowCreateRequest):
    """Lock wholesale funds into escrow using a secure transaction reference and dynamic QR payload."""
    escrow_id = f"esc_{uuid.uuid4().hex[:8]}"
    qr_payload = f"PAYMERCH://SECURE-ESCROW/{escrow_id}/ZAR-{payload.amount_zar}"
    
    escrow_record = {
        "escrow_id": escrow_id,
        **payload.dict(),
        "status": "locked",
        "qr_code_payload": qr_payload
    }
    ESCROWS_DB[escrow_id] = escrow_record
    return {
        "status": "success", 
        "message": "Wholesale funds successfully locked in PayMerch escrow", 
        "escrow": escrow_record
    }

@router.post("/escrow/release")
def release_escrow(payload: EscrowReleaseRequest):
    """Release escrow funds to the wholesaler account upon verified physical delivery."""
    if payload.escrow_id not in ESCROWS_DB:
        raise HTTPException(status_code=404, detail="Escrow transaction reference not found.")
    
    escrow = ESCROWS_DB[payload.escrow_id]
    if not payload.delivery_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Delivery verification required prior to escrow fund release."
        )
    
    escrow["status"] = "released"
    return {
        "status": "success", 
        "message": "Escrow funds successfully disbursed to wholesaler account.", 
        "escrow_id": payload.escrow_id,
        "disbursed_amount_zar": escrow["amount_zar"]
    }