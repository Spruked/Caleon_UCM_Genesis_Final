"""
Phi-3 Linguistic Utility Node for Cerebral Cortex

This module provides linguistic co-processing capabilities within the Cerebral Cortex.
Phi-3 serves as a utility for primitive inference, text transformations, and structural bridging.

NOT the cognition engine - just one linguistic tool among many cognitive modules.
"""
import httpx
import asyncio
import json
import logging
from typing import AsyncGenerator


OLLAMA_URL = "http://localhost:11434/api/generate"

async def generate(prompt: str):
    """
    Phi-3 linguistic utility: Generate primitive inferences and text transformations.
    
    Used by Cerebral Cortex for:
    - Short-form generative conversions
    - Linguistic compressions/expansions
    - Structural bridging between concepts
    - Primitive inference support
    """
    logging.info(f"[PHI3 UTILITY] Linguistic request: {prompt}")

    response = None
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "dtype": "float32"  # Force float32 for CPU compatibility
                    }
                }
            )

        # Log raw text always
        logging.info(f"[PHI3 UTILITY] Raw linguistic output: {response.text}")

        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    
    except Exception as e:
        logging.error(f"[PHI3 UTILITY] Linguistic processing error: {e}", exc_info=True)
        if response:
            logging.error(f"[PHI3 UTILITY] Response text: {response.text}")
        else:
            logging.error("[PHI3 UTILITY] No response text available")
        raise


class Phi3Client:
    """Linguistic utility client for Phi-3 Mini via Ollama API"""

    def __init__(self, endpoint: str = "http://localhost:11434"):
        self.endpoint = endpoint

    async def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Generate a complete response from Phi-3 Mini"""
        return await generate(prompt)

    async def stream_generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7):
        """Stream response from Phi-3 Mini token by token"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.endpoint}/api/generate",
                    json={
                        "model": "phi3",
                        "prompt": prompt,
                        "stream": True,
                        "options": {
                            "temperature": temperature,
                            "max_tokens": max_tokens,
                            "dtype": "float32"  # Force float32 for CPU compatibility
                        }
                    }
                ) as response:
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                                if data.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logging.error(f"Phi-3 streaming error: {e}")
            yield "Processing this request requires additional cognitive resources."


# Global client instance
phi3_client = Phi3Client()