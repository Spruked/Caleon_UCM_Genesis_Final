"""
beneficiary_exclusions.py
--------------------------------
Defines individuals who are excluded from receiving any benefits,
payouts, distributions, access privileges, or financial gain from
Bryan's companies, applications, systems, or digital assets.

This is NOT a punitive system.
It does NOT interact with these individuals in any way.
It does NOT target or monitor anyone.
It simply omits specified individuals from internal benefit flows.

Purpose: Peaceful omission.
"""

from typing import Set


# Permanent exclusion list (case-insensitive)
EXCLUDED_BENEFICIARIES: Set[str] = {
    "angela dian alexander bennett",
    "karen alexander",
}


def normalize(name: str) -> str:
    """Normalize a name string for consistent comparison."""
    return name.strip().lower()


def is_excluded(name: str) -> bool:
    """
    Returns True if the individual is excluded from receiving
    benefits or participation in company systems.

    Silent, neutral, and internal-only.
    """
    return normalize(name) in EXCLUDED_BENEFICIARIES