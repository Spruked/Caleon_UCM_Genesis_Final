"""
ISS Module Integration Routes
=============================

FastAPI routes for ISS Module and Cali X One integration.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from iss_client import get_iss_client, ISSClient

router = APIRouter(prefix="/iss", tags=["iss-integration"])

@router.get("/health")
async def iss_health_check(iss_client: ISSClient = Depends(get_iss_client)):
    """Check ISS Module health"""
    health_data = await iss_client.health_check()
    return {
        "ucm_status": "connected",
        "iss_module": health_data,
        "integration": "active"
    }

@router.post("/cali/voice/test")
async def test_cali_voice(message: str, user: str = "ucm_user", iss_client: ISSClient = Depends(get_iss_client)):
    """Test Cali X One voice interaction"""
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    result = await iss_client.cali_voice_test(message, user)
    return {
        "ucm_bridge": "active",
        "cali_response": result
    }

@router.get("/cali/signature")
async def cali_signature_status(iss_client: ISSClient = Depends(get_iss_client)):
    """Check Cali X One signature status"""
    signature_data = await iss_client.cali_signature_status()
    return {
        "ucm_bridge": "active",
        "cali_signature": signature_data
    }

@router.get("/stardate")
async def get_stardate(iss_client: ISSClient = Depends(get_iss_client)):
    """Get current stardate from ISS Module"""
    stardate_data = await iss_client.get_stardate()
    return {
        "ucm_timestamp": "active",
        "stardate": stardate_data
    }

@router.get("/status")
async def full_integration_status(iss_client: ISSClient = Depends(get_iss_client)):
    """Get full UCM-ISS-Cali integration status"""
    health = await iss_client.health_check()
    signature = await iss_client.cali_signature_status()
    stardate = await iss_client.get_stardate()

    return {
        "ucm_core": {
            "status": "active",
            "version": "2.0.0",
            "port": 8080
        },
        "iss_module": {
            "status": health.get("status", "unknown"),
            "port": 8003,
            "cali_x_one": signature.get("signed", False)
        },
        "integration": {
            "bridge": "active",
            "stardate": stardate,
            "last_check": "now"
        }
    }