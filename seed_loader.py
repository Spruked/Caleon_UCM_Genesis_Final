"""
Centralized Seed Loader for UCM
All seed vault calls should go through this module.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

class CentralizedSeedLoader:
    def __init__(self, seed_root: Path = None):
        self.seed_root = seed_root or Path(__file__).parent / "seeds"
    
    def load_seed(self, seed_name: str) -> Dict[str, Any]:
        """Load a specific seed by name"""
        seed_file = self.seed_root / f"{seed_name}.json"
        if not seed_file.exists():
            raise FileNotFoundError(f"Seed {seed_name} not found")
        
        with open(seed_file, 'r') as f:
            return json.load(f)
    
    def load_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """Load all seeds for a category"""
        category_seeds = {}
        pattern = f"seed_{category}_*.json"
        for file in self.seed_root.glob(pattern):
            with open(file, 'r') as f:
                seed_name = file.stem
                category_seeds[seed_name] = json.load(f)
        return category_seeds
    
    def list_seeds(self) -> List[str]:
        """List all available seed names"""
        return [f.stem for f in self.seed_root.glob("*.json")]

# Global instance
seed_loader = CentralizedSeedLoader()