# cognition/skg/__init__.py  –  clean, final version (Dec 2025)

from .core import SKGCore
from .core import SKGService
from .core import Knowledge   # if you use the client class directly

__all__ = ["SKGCore", "SKGService", "Knowledge"]