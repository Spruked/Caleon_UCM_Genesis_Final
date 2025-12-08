"""
EchoStack - Resonance processing module for Caleon 2.0 Core Reasoning System
Implements echo chamber logic with compression trees and resonance patterns.
"""
import time
import random
from typing import Dict, Any, List
import hashlib

class EchoStack:
    """
    EchoStack - Resonance processing with echo chamber logic

    Implements:
    • Echo chamber pattern recognition
    • Resonance tree compression
    • Feedback loop processing
    • Temporal echo analysis
    """

    def __init__(self, trailing_ms: int = 0, randomize_logic: bool = False):
        self.trailing_ms = trailing_ms
        self.randomize_logic = randomize_logic
        self.echo_history = []
        self.resonance_trees = []
        self.compression_ratio = 0.7

        if randomize_logic:
            random.seed(int(time.time() * 1000) % 10000)

    def process(self, pyramid_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        CaleonCore interface: Process pyramid output through echo stack logic.

        Args:
            pyramid_output: Dict from SynapticResonator.pyramid_distill()

        Returns:
            Dict containing resonance payload with echo analysis
        """
        resonance_packet = pyramid_output.get("resonance_packet", {})
        pulse_id = pyramid_output.get("pulse_id", 0)
        confidence = pyramid_output.get("confidence", 0.5)

        # Apply trailing delay if configured
        if self.trailing_ms > 0:
            time.sleep(self.trailing_ms / 1000.0)

        # Process through echo chamber logic
        echo_analysis = self._process_echo_chamber(resonance_packet)
        resonance_tree = self._build_resonance_tree(echo_analysis)
        compressed_tree = self._compress_resonance_tree(resonance_tree)

        # Store in echo history
        echo_entry = {
            "pulse_id": pulse_id,
            "timestamp": time.time(),
            "echo_analysis": echo_analysis,
            "resonance_tree": compressed_tree,
            "confidence": confidence
        }
        self.echo_history.append(echo_entry)

        # Return standardized resonance payload
        return {
            "resonance_payload": compressed_tree,
            "echo_strength": echo_analysis.get("echo_strength", 0.5),
            "feedback_loops": echo_analysis.get("feedback_loops", 0),
            "pulse_id": pulse_id,
            "module": "echo_stack",
            "compression_ratio": self.compression_ratio,
            "trailing_delay": self.trailing_ms
        }

    def _process_echo_chamber(self, resonance_packet: Dict[str, Any]) -> Dict[str, Any]:
        """Process resonance through echo chamber pattern recognition"""
        layers = resonance_packet.get("layers", {})
        raw_layer = layers.get("raw", {})
        temporal_layer = layers.get("temporal", {})

        # Analyze echo patterns
        echo_patterns = self._analyze_echo_patterns(raw_layer, temporal_layer)
        feedback_loops = self._detect_feedback_loops(echo_patterns)
        echo_strength = self._compute_echo_strength(echo_patterns, feedback_loops)

        # Apply randomization if enabled
        if self.randomize_logic:
            echo_strength *= random.uniform(0.8, 1.2)
            feedback_loops = int(feedback_loops * random.uniform(0.9, 1.1))

        return {
            "echo_patterns": echo_patterns,
            "feedback_loops": feedback_loops,
            "echo_strength": echo_strength,
            "pattern_complexity": len(echo_patterns),
            "randomized": self.randomize_logic
        }

    def _analyze_echo_patterns(self, raw: Dict[str, Any], temporal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze resonance patterns for echo characteristics"""
        patterns = []

        # Extract pattern signatures
        signal_hash = raw.get("signal_hash", "")
        complexity = raw.get("complexity", 0.5)
        temporal_coherence = temporal.get("temporal_coherence", 0)

        # Generate echo patterns based on signal characteristics
        pattern_count = max(1, int(complexity * 10))

        for i in range(pattern_count):
            pattern_hash = hashlib.md5(f"{signal_hash}_{i}".encode()).hexdigest()
            pattern = {
                "pattern_id": f"echo_{i}",
                "signature": pattern_hash[:16],
                "strength": float(int(pattern_hash[:2], 16)) / 255.0,
                "frequency": temporal_coherence + i,
                "resonance": complexity * (1 + i * 0.1)
            }
            patterns.append(pattern)

        return patterns

    def _detect_feedback_loops(self, patterns: List[Dict[str, Any]]) -> int:
        """Detect feedback loops in echo patterns"""
        loops = 0

        for i, pattern in enumerate(patterns):
            strength = pattern.get("strength", 0.0)
            frequency = pattern.get("frequency", 0)

            # Simple feedback detection: high strength + high frequency
            if strength > 0.7 and frequency > 5:
                loops += 1

        return loops

    def _compute_echo_strength(self, patterns: List[Dict[str, Any]], feedback_loops: int) -> float:
        """Compute overall echo strength"""
        if not patterns:
            return 0.0

        avg_strength = sum(p.get("strength", 0.0) for p in patterns) / len(patterns)
        loop_bonus = min(0.3, feedback_loops * 0.1)

        return min(1.0, avg_strength + loop_bonus)

    def _build_resonance_tree(self, echo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Build hierarchical resonance tree from echo analysis"""
        patterns = echo_analysis.get("echo_patterns", [])

        # Build tree structure
        tree = {
            "root": {
                "strength": echo_analysis.get("echo_strength", 0.5),
                "feedback_loops": echo_analysis.get("feedback_loops", 0),
                "children": []
            }
        }

        # Add patterns as tree nodes
        for pattern in patterns[:5]:  # Limit to top 5 patterns
            node = {
                "pattern_id": pattern["pattern_id"],
                "strength": pattern["strength"],
                "resonance": pattern["resonance"],
                "children": []
            }
            tree["root"]["children"].append(node)

        return tree

    def _compress_resonance_tree(self, tree: Dict[str, Any]) -> Dict[str, Any]:
        """Compress resonance tree using compression ratio"""
        if self.compression_ratio >= 1.0:
            return tree

        # Simple compression: reduce node counts
        compressed = tree.copy()

        if "root" in compressed and "children" in compressed["root"]:
            original_count = len(compressed["root"]["children"])
            keep_count = max(1, int(original_count * self.compression_ratio))
            compressed["root"]["children"] = compressed["root"]["children"][:keep_count]
            compressed["compression_applied"] = True
            compressed["original_nodes"] = original_count
            compressed["compressed_nodes"] = keep_count

        return compressed

    def get_echo_history(self) -> List[Dict[str, Any]]:
        """Get echo processing history"""
        return self.echo_history.copy()

    def clear_echo_history(self):
        """Clear echo processing history"""
        self.echo_history.clear()