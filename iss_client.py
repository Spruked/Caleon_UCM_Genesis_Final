"""
ISS Module Client for UCM Integration
=====================================

Client for connecting UCM to ISS Module and Cali X One services.
"""

import httpx
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class CaliVoiceRequest(BaseModel):
    message: str
    user: Optional[str] = "ucm_user"
    session_id: Optional[str] = None

class ISSClient:
    """Client for ISS Module and Cali X One integration"""

    def __init__(self, iss_host: str = "localhost", iss_port: int = 8003):
        self.base_url = f"http://{iss_host}:{iss_port}"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def health_check(self) -> Dict[str, Any]:
        """Check ISS Module health"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"ISS health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

    async def cali_voice_test(self, message: str, user: str = "ucm_user") -> Dict[str, Any]:
        """Test Cali X One voice interaction"""
        try:
            request_data = CaliVoiceRequest(message=message, user=user)
            response = await self.client.post(
                f"{self.base_url}/cali/voice/test",
                json=request_data.dict()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Cali voice test failed: {e}")
            return {"error": str(e), "status": "failed"}

    async def cali_signature_status(self) -> Dict[str, Any]:
        """Check Cali X One signature status"""
        try:
            response = await self.client.get(f"{self.base_url}/cali/signature/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Cali signature check failed: {e}")
            return {"signed": False, "error": str(e)}

    async def get_stardate(self) -> Dict[str, Any]:
        """Get current stardate from ISS Module"""
        try:
            response = await self.client.get(f"{self.base_url}/api/stardate")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Stardate request failed: {e}")
            return {"error": str(e)}

# Global ISS client instance
iss_client = ISSClient()

async def get_iss_client() -> ISSClient:
    """Get ISS client instance"""
    return iss_client