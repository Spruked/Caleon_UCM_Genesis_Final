"""
Synaptic Resonator - Micro-resonator grid for Caleon 2.0 Core Reasoning System
Implements the inverted pyramid distillation and pulse gating logic.
"""
import time
import hashlib
from typing import Dict, Any, List
import numpy as np

class SynapticResonator:
    """
    Micro-resonator grid that processes input signals through an inverted pyramid.
    Distills complex inputs into structured resonance patterns for downstream processing.
    """

    def __init__(self, core_callback=None):
        self.core_callback = core_callback
        self.pulse_counter = 0
        self.resonance_history = []
        self.pyramid_layers = 4  # 4-layer inverted pyramid

    def next_pulse(self) -> int:
        """Generate next pulse ID for signal gating"""
        self.pulse_counter += 1
        return self.pulse_counter

    def pyramid_distill(self, normalized_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process normalized input through inverted pyramid distillation.

        Args:
            normalized_input: Dict with keys: signal, timestamp, pulse, source

        Returns:
            Dict containing distilled resonance patterns
        """
        signal = normalized_input["signal"]
        timestamp = normalized_input["timestamp"]
        pulse = normalized_input["pulse"]
        source = normalized_input["source"]

        # Layer 1: Raw signal resonance (broad capture)
        layer1_resonance = self._compute_signal_resonance(signal)

        # Layer 2: Temporal coherence (pattern recognition)
        layer2_patterns = self._extract_temporal_patterns(layer1_resonance, timestamp)

        # Layer 3: Pulse-gated distillation (attention focusing)
        layer3_focused = self._apply_pulse_gating(layer2_patterns, pulse)

        # Layer 4: Source-attributed synthesis (context integration)
        layer4_synthesis = self._synthesize_with_source(layer3_focused, source)

        # Store in resonance history
        resonance_packet = {
            "pulse_id": pulse,
            "timestamp": timestamp,
            "source": source,
            "layers": {
                "raw": layer1_resonance,
                "temporal": layer2_patterns,
                "gated": layer3_focused,
                "synthesized": layer4_synthesis
            },
            "confidence": self._compute_confidence(layer4_synthesis)
        }

        self.resonance_history.append(resonance_packet)

        # Return pyramid output for downstream modules
        return {
            "resonance_packet": resonance_packet,
            "pyramid_output": layer4_synthesis,
            "pulse_id": pulse,
            "confidence": resonance_packet["confidence"]
        }

    def _compute_signal_resonance(self, signal: Any) -> Dict[str, Any]:
        """Layer 1: Convert signal to resonance patterns"""
        signal_str = str(signal)
        signal_hash = hashlib.md5(signal_str.encode()).hexdigest()

        # Simple resonance based on signal characteristics
        return {
            "signal_hash": signal_hash,
            "length": len(signal_str),
            "complexity": self._estimate_complexity(signal_str),
            "resonance_vector": [ord(c) % 10 for c in signal_hash[:10]]
        }

    def _extract_temporal_patterns(self, resonance: Dict, timestamp: float) -> Dict[str, Any]:
        """Layer 2: Extract temporal coherence patterns"""
        # Look for patterns in recent resonance history
        recent_patterns = self.resonance_history[-5:] if self.resonance_history else []

        return {
            "temporal_coherence": len(recent_patterns),
            "pattern_matches": self._find_pattern_matches(resonance, recent_patterns),
            "temporal_vector": [timestamp % 100, len(recent_patterns), resonance["complexity"]]
        }

    def _apply_pulse_gating(self, patterns: Dict, pulse: int) -> Dict[str, Any]:
        """Layer 3: Apply pulse-gated attention focusing"""
        # Use pulse ID to modulate attention
        pulse_modulator = (pulse % 10) / 10.0

        return {
            "gated_patterns": patterns,
            "attention_weight": pulse_modulator,
            "focus_vector": [pulse_modulator * v for v in patterns["temporal_vector"]]
        }

    def _synthesize_with_source(self, focused: Dict, source: str) -> Dict[str, Any]:
        """Layer 4: Synthesize with source attribution"""
        source_hash = hashlib.md5(source.encode()).hexdigest()
        source_vector = [int(source_hash[i:i+2], 16) % 100 for i in range(0, 10, 2)]

        return {
            "source_vector": source_vector,
            "integrated_patterns": focused,
            "synthesis_score": np.mean(source_vector + focused["focus_vector"])
        }

    def _estimate_complexity(self, signal_str: str) -> float:
        """Estimate signal complexity"""
        if not signal_str:
            return 0.0
        unique_chars = len(set(signal_str))
        return unique_chars / len(signal_str)

    def _find_pattern_matches(self, current: Dict, recent: List) -> int:
        """Find how many recent patterns match current"""
        matches = 0
        for old in recent:
            if old["layers"]["raw"]["signal_hash"][:8] == current["signal_hash"][:8]:
                matches += 1
        return matches

    def _compute_confidence(self, synthesis: Dict) -> float:
        """Compute overall confidence in the distillation"""
        base_confidence = 0.5
        synthesis_score = synthesis.get("synthesis_score", 0) / 100.0
        return min(1.0, base_confidence + synthesis_score)