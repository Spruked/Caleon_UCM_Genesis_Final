#!/usr/bin/env python3
"""
Unified Cognition Module (UCM) - Caleon Prime Service
Standalone FastAPI service that provides unified AI cognition across all apps

This service runs Caleon Prime and exposes her through a stable API
that any application can connect to.

Usage:
    python main.py                    # Run locally on localhost:8000
    docker run -p 8000:8000 ucm      # Run in Docker
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import all UCM components
from api.bubble import router as bubble_router
from api.health import router as health_router

# Create FastAPI app
app = FastAPI(
    title="Unified Cognition Module - Caleon Prime",
    description="Central AI cognition service for all applications",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(bubble_router)
app.include_router(health_router)

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Unified Cognition Module",
        "entity": "Caleon Prime",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health",
            "bubble": "/api/bubble"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Initialize UCM components on startup"""
    print("🚀 Starting Unified Cognition Module...")
    print("🤖 Caleon Prime initializing...")

    # Components are initialized through imports
    # Vault, continuity, Abby protocol, etc. are ready

    print("✅ UCM ready - Caleon Prime online")
    print("📡 Service available at:")
    print("   Local: http://localhost:8000")
    print("   Docker: http://ucm:8000")
    print("   Docs: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down UCM...")
    print("👋 Caleon Prime signing off")

if __name__ == "__main__":
    # Auto-detect environment
    host = os.getenv("UCM_HOST", "0.0.0.0")
    port = int(os.getenv("UCM_PORT", "8000"))

    print(f"🌐 Starting UCM service on {host}:{port}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("UCM_RELOAD", "false").lower() == "true",
        log_level="info"
    )