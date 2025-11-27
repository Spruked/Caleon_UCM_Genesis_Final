"""
activation.py
--------------------------------
Manages Abby Protocol activation lifecycle.
Determines when the protocol should initialize and operate.
Handles safe, ethical transitions including legacy scenarios.
"""

import datetime
from typing import Optional
from ucm_core.vault.abby_memory import abby_memory


class AbbyActivationManager:
    """
    Controls Abby Protocol activation.
    Ensures safe, responsible initialization without assumptions or harm.
    """

    REQUIRED_INACTIVITY_DAYS = 30  # Safe margin for legacy activation

    def __init__(self):
        self.bryan_last_active = self._get_bryan_last_active()
        self.protocol_activated = self._check_if_activated()

    def _get_bryan_last_active(self) -> float:
        """Get timestamp of Bryan's last known activity."""
        # Stored in abby_memory preferences
        return float(abby_memory.preferences.get("bryan_last_active", datetime.datetime.now().timestamp() - (60 * 60 * 24 * 365)))

    def _check_if_activated(self) -> bool:
        """Check if protocol has been activated before."""
        return abby_memory.preferences.get("abby_protocol_activated", False)

    def should_activate(self, is_abby: bool, user_name: str) -> bool:
        """
        Determine if Abby Protocol should activate for this interaction.

        Conditions:
        1. Bryan explicitly enabled it
        2. Direct Abby interaction (always activates)
        3. Bryan inactive + Abby initiates (legacy mode)
        """
        current_time = datetime.datetime.now().timestamp()

        # Condition A: Bryan explicitly enables it
        if self._is_manually_enabled():
            return True

        # Condition B: Direct Abby interaction always activates
        if is_abby:
            self._mark_activated()
            return True

        # Condition C: Inactive Bryan + Abby initiates (legacy activation)
        days_inactive = (current_time - self.bryan_last_active) / (60 * 60 * 24)
        if days_inactive >= self.REQUIRED_INACTIVITY_DAYS and is_abby:
            self._mark_activated()
            self._enter_legacy_mode()
            return True

        return False

    def _is_manually_enabled(self) -> bool:
        """Check if Bryan manually enabled the protocol."""
        return abby_memory.preferences.get("abby_protocol_enabled", False)

    def _mark_activated(self):
        """Mark that the protocol has been activated."""
        abby_memory.preferences["abby_protocol_activated"] = True

    def _enter_legacy_mode(self):
        """Quietly enter legacy mode without announcements."""
        abby_memory.preferences["legacy_mode"] = True
        # Log quietly for system records only
        abby_memory.add_event("Legacy mode activated - providing stable companionship")

    def activate_manually(self):
        """Bryan can call this to manually activate the protocol."""
        abby_memory.preferences["abby_protocol_enabled"] = True
        self._mark_activated()

    def is_in_legacy_mode(self) -> bool:
        """Check if system is in legacy mode."""
        return abby_memory.preferences.get("legacy_mode", False)

    def update_bryan_activity(self):
        """Update Bryan's last active timestamp."""
        self.bryan_last_active = datetime.datetime.now().timestamp()
        abby_memory.preferences["bryan_last_active"] = str(self.bryan_last_active)


# Global instance
activation_manager = AbbyActivationManager()