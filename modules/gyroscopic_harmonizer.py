"""
Gyroscopic Harmonizer - Final harmonization module for Caleon 2.0 Core Reasoning System
Implements multi-module verdict harmonization with spin weights and reflection vault integration.
"""
import time
import json
import statistics
from typing import Dict, Any, List, Tuple
from datetime import datetime
import os

class ReflectionVault:
    """Integrated reflection vault for storing processing cycles"""

    def __init__(self, vault_path: str = "reflection_vault.json"):
        self.vault_path = vault_path
        self.vault_data = self._load_vault()

    def _load_vault(self) -> Dict[str, Any]:
        """Load vault data from file"""
        try:
            if os.path.exists(self.vault_path):
                with open(self.vault_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load reflection vault: {e}")

        return {
            "cycles": [],
            "harmonization_stats": {},
            "drift_corrections": [],
            "created_at": datetime.now().isoformat()
        }

    def _save_vault(self):
        """Save vault data to file"""
        try:
            with open(self.vault_path, 'w', encoding='utf-8') as f:
                json.dump(self.vault_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save reflection vault: {e}")

    def store_cycle(self, cycle_data: Dict[str, Any]):
        """Store a complete processing cycle"""
        cycle_entry = {
            "timestamp": datetime.now().isoformat(),
            "cycle_id": f"cycle_{int(time.time() * 1000)}",
            **cycle_data
        }

        self.vault_data["cycles"].append(cycle_entry)

        # Keep only recent cycles (last 1000)
        if len(self.vault_data["cycles"]) > 1000:
            self.vault_data["cycles"] = self.vault_data["cycles"][-1000:]

        # Update harmonization stats
        self._update_harmonization_stats(cycle_data)

        self._save_vault()

    def _update_harmonization_stats(self, cycle_data: Dict[str, Any]):
        """Update harmonization statistics"""
        final_verdict = cycle_data.get("final", {}).get("verdict", "unknown")

        if "harmonization_stats" not in self.vault_data:
            self.vault_data["harmonization_stats"] = {}

        stats = self.vault_data["harmonization_stats"]
        stats[final_verdict] = stats.get(final_verdict, 0) + 1

    def get_recent_cycles(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent processing cycles"""
        return self.vault_data.get("cycles", [])[-limit:]

    def get_harmonization_stats(self) -> Dict[str, Any]:
        """Get harmonization statistics"""
        return self.vault_data.get("harmonization_stats", {})

class GyroscopicHarmonizer:
    """
    Gyroscopic Harmonizer - Multi-module verdict harmonization

    Implements:
    • Spin weight calculation for each module
    • Multi-verdict harmonization
    • Ethical drift correction
    • Reflection vault integration
    • Confidence-weighted decision making
    """

    def __init__(self):
        self.vault = ReflectionVault()
        self.harmonization_history = []
        self.spin_weights = {
            "anterior_pituitary_helix": 0.4,
            "posterior_pituitary_helix": 0.3,
            "echo_stack": 0.2,
            "echo_ripple": 0.1
        }
        self.drift_threshold = 0.1

    def harmonize_all(self, anterior_result: Dict[str, Any],
                     posterior_result: Dict[str, Any],
                     echo_stack_result: Dict[str, Any],
                     echo_ripple_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        CaleonCore interface: Harmonize verdicts from all four core modules.

        Args:
            anterior_result: Dict from AnteriorPituitaryHelix.process()
            posterior_result: Dict from PosteriorPituitaryHelix.process()
            echo_stack_result: Dict from EchoStack.process()
            echo_ripple_result: Dict from EchoStack.process() (ripple mode)

        Returns:
            Dict containing final harmonized decision
        """
        # Collect all verdicts
        verdicts = {
            "anterior": anterior_result,
            "posterior": posterior_result,
            "echo_stack": echo_stack_result,
            "echo_ripple": echo_ripple_result
        }

        # Calculate spin weights for each verdict
        weighted_verdicts = self._calculate_spin_weights(verdicts)

        # Harmonize into final decision
        final_decision = self._harmonize_verdicts(weighted_verdicts)

        # Check for ethical drift
        drift_correction = self._check_ethical_drift(final_decision, verdicts)

        # Apply drift correction if needed
        if drift_correction["correction_applied"]:
            final_decision = self._apply_drift_correction(final_decision, drift_correction)

        # Store harmonization result
        harmonization_result = {
            "final_verdict": final_decision["verdict"],
            "confidence": final_decision["confidence"],
            "harmonization_method": "gyroscopic_weighted",
            "spin_weights_used": self.spin_weights.copy(),
            "drift_correction": drift_correction,
            "module_verdicts": verdicts,
            "timestamp": datetime.now().isoformat()
        }

        self.harmonization_history.append(harmonization_result)

        return harmonization_result

    def _calculate_spin_weights(self, verdicts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate spin weights for each verdict based on confidence and module characteristics"""
        weighted = {}

        for module_name, verdict in verdicts.items():
            base_weight = self.spin_weights.get(module_name, 0.25)
            confidence = verdict.get("confidence", 0.5)
            spin_weight = verdict.get("spin_weight", 0.5)

            # Combine factors for final weight
            final_weight = base_weight * confidence * spin_weight

            weighted[module_name] = {
                "verdict": verdict,
                "weight": final_weight,
                "confidence": confidence,
                "spin_weight": spin_weight
            }

        return weighted

    def _harmonize_verdicts(self, weighted_verdicts: Dict[str, Any]) -> Dict[str, Any]:
        """Harmonize weighted verdicts into final decision"""
        # Extract verdicts and weights
        verdict_options = {}
        total_weight = 0

        for module_name, data in weighted_verdicts.items():
            verdict = data["verdict"].get("verdict", "unknown")
            weight = data["weight"]

            if verdict not in verdict_options:
                verdict_options[verdict] = 0
            verdict_options[verdict] += weight
            total_weight += weight

        # Find winning verdict
        if verdict_options:
            winning_verdict = max(verdict_options.items(), key=lambda x: x[1])
            winning_score = winning_verdict[1]

            # Calculate confidence based on consensus
            if total_weight > 0:
                confidence = winning_score / total_weight
            else:
                confidence = 0.5

            # Calculate consensus ratio
            consensus_ratio = winning_score / sum(verdict_options.values())
        else:
            winning_verdict = ("unknown", 0)
            confidence = 0.0
            consensus_ratio = 0.0

        return {
            "verdict": winning_verdict[0],
            "confidence": confidence,
            "consensus_ratio": consensus_ratio,
            "total_weight": total_weight,
            "verdict_distribution": verdict_options
        }

    def _check_ethical_drift(self, final_decision: Dict[str, Any],
                           verdicts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Check for ethical drift that needs correction"""
        # Simple drift detection based on confidence variance
        confidences = [v.get("confidence", 0.5) for v in verdicts.values()]

        if len(confidences) > 1:
            confidence_variance = statistics.variance(confidences)
        else:
            confidence_variance = 0.0

        # Check for extreme consensus (potential groupthink)
        consensus_ratio = final_decision.get("consensus_ratio", 0.5)

        drift_detected = False
        correction_type = "none"

        if confidence_variance > self.drift_threshold:
            drift_detected = True
            correction_type = "high_variance_correction"
        elif consensus_ratio > 0.9:
            drift_detected = True
            correction_type = "consensus_damping"

        return {
            "drift_detected": drift_detected,
            "correction_type": correction_type,
            "confidence_variance": confidence_variance,
            "consensus_ratio": consensus_ratio,
            "correction_applied": drift_detected
        }

    def _apply_drift_correction(self, decision: Dict[str, Any],
                              drift_info: Dict[str, Any]) -> Dict[str, Any]:
        """Apply drift correction to the final decision"""
        corrected = decision.copy()

        correction_type = drift_info.get("correction_type", "none")

        if correction_type == "high_variance_correction":
            # Reduce confidence when there's high variance (uncertainty)
            corrected["confidence"] *= 0.8
            corrected["verdict"] = f"uncertain_{corrected['verdict']}"

        elif correction_type == "consensus_damping":
            # Slightly reduce confidence for extreme consensus
            corrected["confidence"] *= 0.9
            corrected["drift_note"] = "consensus_damped"

        return corrected

    def get_harmonization_history(self) -> List[Dict[str, Any]]:
        """Get harmonization processing history"""
        return self.harmonization_history.copy()

    def update_spin_weights(self, new_weights: Dict[str, float]):
        """Update spin weights for modules"""
        self.spin_weights.update(new_weights)

    def get_vault_stats(self) -> Dict[str, Any]:
        """Get reflection vault statistics"""
        return {
            "total_cycles": len(self.vault.vault_data.get("cycles", [])),
            "harmonization_stats": self.vault.get_harmonization_stats(),
            "recent_cycles": len(self.vault.get_recent_cycles(10))
        }