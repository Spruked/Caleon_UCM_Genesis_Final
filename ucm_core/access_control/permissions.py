"""
permissions.py
--------------------------------
System-wide access control for UCM Genesis.
Integrates beneficiary exclusions for silent omission.
"""

from ucm_core.access_control.beneficiary_exclusions import is_excluded


def has_system_access(user_name: str) -> bool:
    """
    Determines if a user has access to the system.
    Excluded beneficiaries are silently denied access.
    """
    if is_excluded(user_name):
        return False
    return True


def can_receive_benefits(user_name: str) -> bool:
    """
    Determines if a user can receive any benefits, payouts, or distributions.
    Excluded beneficiaries are silently omitted.
    """
    return not is_excluded(user_name)