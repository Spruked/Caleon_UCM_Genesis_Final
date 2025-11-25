from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
from pathlib import Path

router = APIRouter(prefix="/api/seed_vault")

# Centralized seed vault location
SEED_ROOT = Path(__file__).parent.parent / "seeds"

@router.get("/get/{seed_name}")
async def get_seed(seed_name: str):
    """Get a specific seed by name"""
    seed_file = SEED_ROOT / f"{seed_name}.json"
    if not seed_file.exists():
        raise HTTPException(status_code=404, detail=f"Seed {seed_name} not found")
    
    with open(seed_file, 'r') as f:
        return json.load(f)

@router.get("/list")
async def list_seeds():
    """List all available seeds"""
    seeds = []
    for file in SEED_ROOT.glob("*.json"):
        seeds.append(file.stem)
    return {"seeds": seeds}

@router.post("/load_category/{category}")
async def load_category(category: str):
    """Load all seeds for a category (philosopher, system, etc.)"""
    category_seeds = {}
    for file in SEED_ROOT.glob(f"seed_{category}_*.json"):
        with open(file, 'r') as f:
            seed_name = file.stem
            category_seeds[seed_name] = json.load(f)
    return category_seeds