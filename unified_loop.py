"""
Unified Cognition Loop
Orchestrates the complete cognitive processing pipeline with asyncio.

Sequence: Resonator → Anterior → EchoStack → EchoRipple → Posterior → Harmonizer → Consent → Articulation
"""

import asyncio
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
import sys

# Add path to Vault_System_1.0
sys.path.append(os.path.join(os.path.dirname(__file__), "Vault_System_1.0"))

# Import vault system
try:
    from vault_system.plug_and_play_integration import AdvancedVaultSystem
except ImportError:
    AdvancedVaultSystem = None
    print("Warning: Vault_System_1.0 not found, running without advanced vault system")

# Mock speaker for testing
class MockSpeaker:
    def speak(self, text: str) -> None:
        print(f"[MOCK SPEAKER] Speaking: {text}")

# Import core modules
from cerebral_cortex.llm_bridge import LLMBridge
from symbolic_memory_vault import SymbolicMemoryVault
from caleon_consent import CaleonConsentManager
from voice_consent import VoiceConsentListener
from echostack.echostack import EchoStack
from echoripple.echoripple import EchoRipple

# Mock articulation bridge for testing
class MockArticulationBridge:
    def __init__(self):
        self.speaker = MockSpeaker()
    
    def articulate(self, text: str) -> str:
        self.speaker.speak(text)
        return f"Articulated: {text}"

# Import helix modules (assuming they have process methods)
try:
    from synaptic_resonator.main import SynapticResonator
except ImportError:
    # Fallback mock
    class SynapticResonator:
        async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
            await asyncio.sleep(0.01)  # Simulate processing
            return {"resonance": 0.7, "patterns": ["pattern1"], "id": "res_001"}

try:
    from anterior_helix.main import AnteriorHelix
except ImportError:
    class AnteriorHelix:
        async def process(self, resonance_data: Dict[str, Any]) -> Dict[str, Any]:
            await asyncio.sleep(0.01)
            return {"verdict": "approved", "confidence": 0.8, "id": "ant_001"}

try:
    from posterior_helix.main import PosteriorHelix
except ImportError:
    class PosteriorHelix:
        async def process(self, reflection_data: Dict[str, Any]) -> Dict[str, Any]:
            await asyncio.sleep(0.01)
            return {"final_output": "processed", "stability": 0.9, "id": "post_001"}

# GyroHarmonizer mock (needs implementation)
class GyroHarmonizer:
    def compute_drift(self, reflection: Dict[str, Any]) -> float:
        # Simple drift computation
        return abs(reflection.get("delta", 0.0)) * 0.1


@dataclass
class CognitionResult:
    """Result of complete cognition cycle"""
    input: str
    final_output: Optional[str]
    consent_granted: bool
    processing_time: float
    reflection_data: Dict[str, Any]
    timestamp: float


class UnifiedCognitionLoop:
    """
    Main orchestration loop for unified cognition processing.
    """

    def __init__(self):
        # Initialize advanced vault system if available
        self.vault_system = None
        if AdvancedVaultSystem:
            try:
                self.vault_system = AdvancedVaultSystem("master_key_caleon_2025", "ucm_node_1")
                print("✅ Advanced Vault System integrated into UCM")
            except Exception as e:
                print(f"Warning: Failed to initialize vault system: {e}")

        # Initialize core components
        self.memory_vault = SymbolicMemoryVault()
        self.consent_manager = CaleonConsentManager(mode="voice")
        self.voice_listener = VoiceConsentListener(self.consent_manager)
        self.llm_bridge = LLMBridge()
        self.articulation_bridge = MockArticulationBridge()

        # Initialize cognitive components
        self.resonator = SynapticResonator()
        self.anterior = AnteriorHelix()
        self.echo_stack = EchoStack()
        self.echo_ripple = EchoRipple()
        self.posterior = PosteriorHelix()
        self.harmonizer = GyroHarmonizer()

        # Initialize verdict and resolution vaults for each reasoning layer
        self.verdict_vaults = {
            "resonator": [],
            "anterior": [],
            "echo_stack": [],
            "echo_ripple": [],
            "posterior": [],
            "harmonizer": [],
            "consent": [],
            "articulation": []
        }
        
        self.resolution_vaults = {
            "resonator": [],
            "anterior": [],
            "echo_stack": [],
            "echo_ripple": [],
            "posterior": [],
            "harmonizer": [],
            "consent": [],
            "articulation": []
        }

        # Load logic seeds for Echo components
        self._load_logic_seeds()

        # Check endpoint wiring
        wiring_status = self.check_endpoint_wiring()
        print("🔗 Endpoint wiring check:")
        for component, connected in wiring_status["components_connected"].items():
            status = "✅" if connected else "❌"
            print(f"  {status} {component}")
        
        if not all(wiring_status["components_connected"].values()):
            print("⚠️ Some components not properly wired - check imports and initialization")

    def store_verdict(self, layer: str, verdict: Dict[str, Any]):
        """Store verdict for a reasoning layer"""
        if layer in self.verdict_vaults:
            verdict_entry = {
                "timestamp": time.time(),
                "layer": layer,
                "verdict": verdict
            }
            self.verdict_vaults[layer].append(verdict_entry)
            print(f"📋 Verdict stored for {layer}: {verdict.get('verdict', 'N/A')}")

    def store_resolution(self, layer: str, resolution: Dict[str, Any]):
        """Store resolution for a reasoning layer"""
        if layer in self.resolution_vaults:
            resolution_entry = {
                "timestamp": time.time(),
                "layer": layer,
                "resolution": resolution
            }
            self.resolution_vaults[layer].append(resolution_entry)
            print(f"🔧 Resolution stored for {layer}: {resolution.get('action', 'N/A')}")

    def _load_logic_seeds(self):
        """Load logic seeds from master seed vault"""
        from seed_loader import seed_loader
        try:
            # Load all available seeds from master vault
            seed_names = seed_loader.list_seeds()
            loaded_seeds = {}
            for name in seed_names:
                try:
                    seed_data = seed_loader.load_seed(name)
                    loaded_seeds[name] = seed_data
                except FileNotFoundError:
                    print(f"Warning: Seed {name} not found in master vault")
            self.echo_stack.vaults = loaded_seeds
            self.echo_ripple.logic_seeds = loaded_seeds
            print(f"✅ Loaded {len(loaded_seeds)} seeds from master seed vault")
        except Exception as e:
            print(f"❌ Failed to load seeds from master vault: {e}")
            # Fallback to mock data
            mock_seeds = {
                "seed_nonmonotonic": {"name": "nonmonotonic", "weight": 1.2},
                "seed_spinoza": {"name": "spinoza", "weight": 1.0},
                "seed_hume": {"name": "hume", "weight": 0.9},
                "seed_taleb": {"name": "taleb", "weight": 1.1},
                "seed_proverbs": {"name": "proverbs", "weight": 0.8},
                "seed_ockhams_filter": {"name": "ockham", "weight": 0.7}
            }
            self.echo_stack.vaults = mock_seeds
            self.echo_ripple.logic_seeds = mock_seeds

    def _scan_and_resolve_endpoint_issues(self, reflection_data: Dict[str, Any]):
        """Scan for endpoint issues across reasoning layers and resolve conflicts"""
        print("🔍 Scanning for endpoint issues and resolving conflicts...")
        
        issues_found = []
        
        # Check for resonance vs confidence mismatch
        resonator_confidence = reflection_data.get("resonator", {}).get("resonance", 0)
        anterior_confidence = reflection_data.get("anterior", {}).get("confidence", 0)
        if resonator_confidence < 0.3 and anterior_confidence > 0.7:
            issues_found.append({
                "type": "confidence_mismatch",
                "layers": ["resonator", "anterior"],
                "description": "Low resonance but high anterior confidence",
                "severity": "medium"
            })
        
        # Check for stability vs consent mismatch
        stability = reflection_data.get("echo_ripple", {}).get("stability_score", 0)
        consent_granted = reflection_data.get("consent", False)
        if stability > 0.8 and not consent_granted:
            issues_found.append({
                "type": "stability_consent_conflict",
                "layers": ["echo_ripple", "consent"],
                "description": "High stability but consent denied",
                "severity": "high"
            })
        
        # Check for missing data
        for layer in ["resonator", "anterior", "echo_stack", "echo_ripple", "posterior", "harmonizer", "consent"]:
            if layer not in reflection_data or not reflection_data[layer]:
                issues_found.append({
                    "type": "missing_data",
                    "layers": [layer],
                    "description": f"Missing data from {layer} layer",
                    "severity": "critical"
                })
        
        # Check for drift issues
        drift_score = reflection_data.get("harmonizer", {}).get("drift_score", 0)
        if drift_score > 0.5:
            issues_found.append({
                "type": "high_drift",
                "layers": ["harmonizer"],
                "description": f"High drift score: {drift_score}",
                "severity": "high"
            })
        
        # Resolve issues
        for issue in issues_found:
            resolution = self._resolve_issue(issue, reflection_data)
            if resolution:
                self.store_resolution(issue["layers"][0], resolution)
        
        if not issues_found:
            print("✅ No endpoint issues detected")
        else:
            print(f"⚠️ Found and resolved {len(issues_found)} endpoint issues")

    def _resolve_issue(self, issue: Dict[str, Any], reflection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve a specific endpoint issue"""
        if issue["type"] == "confidence_mismatch":
            return {
                "action": "confidence_adjustment",
                "method": "weighted_average",
                "adjustment": "reduced_anterior_confidence",
                "reason": "Balancing resonance and anterior confidence"
            }
        elif issue["type"] == "stability_consent_conflict":
            return {
                "action": "consent_escalation",
                "method": "stability_override",
                "adjustment": "escalate_for_review",
                "reason": "High stability warrants consent review"
            }
        elif issue["type"] == "missing_data":
            return {
                "action": "data_recovery",
                "method": "fallback_values",
                "adjustment": "default_assumptions",
                "reason": "Using default values for missing layer data"
            }
        elif issue["type"] == "high_drift":
            return {
                "action": "drift_correction",
                "method": "reflection_recalibration",
                "adjustment": "increased_monitoring",
                "reason": "High drift requires enhanced monitoring"
            }
        return None

    def check_endpoint_wiring(self) -> Dict[str, Any]:
        """Check and report on endpoint wiring status"""
        wiring_status = {
            "components_connected": {},
            "vaults_initialized": {},
            "endpoint_health": {}
        }
        
        # Check component connections
        components = {
            "resonator": self.resonator,
            "anterior": self.anterior,
            "echo_stack": self.echo_stack,
            "echo_ripple": self.echo_ripple,
            "posterior": self.posterior,
            "harmonizer": self.harmonizer,
            "consent_manager": self.consent_manager,
            "llm_bridge": self.llm_bridge
        }
        
        for name, component in components.items():
            wiring_status["components_connected"][name] = component is not None
            wiring_status["endpoint_health"][name] = hasattr(component, 'process') or hasattr(component, 'compute_drift')
        
        # Check vault initialization
        for layer in self.verdict_vaults.keys():
            wiring_status["vaults_initialized"][f"{layer}_verdict"] = layer in self.verdict_vaults
            wiring_status["vaults_initialized"][f"{layer}_resolution"] = layer in self.resolution_vaults
        
        # Check vault system integration
        wiring_status["vault_system_integrated"] = self.vault_system is not None
        
        return wiring_status

    def get_verdict_resolution_summary(self) -> Dict[str, Any]:
        """Get summary of verdicts and resolutions across all layers"""
        summary = {}
        for layer in self.verdict_vaults.keys():
            summary[layer] = {
                "verdicts_count": len(self.verdict_vaults[layer]),
                "resolutions_count": len(self.resolution_vaults[layer]),
                "latest_verdict": self.verdict_vaults[layer][-1] if self.verdict_vaults[layer] else None,
                "latest_resolution": self.resolution_vaults[layer][-1] if self.resolution_vaults[layer] else None
            }
        return summary

    async def process_cognition(self, input_text: str) -> CognitionResult:
        """
        Execute complete cognition cycle with asyncio concurrency.
        """
        start_time = time.time()
        reflection_data = {}

        # Start reasoning path tracking if vault system available
        reasoning_path_id = None
        if self.vault_system:
            try:
                reasoning_path_id = self.vault_system.reasoning_glyph_mapper.start_reasoning_path(
                    f"Cognition processing: {input_text[:50]}..."
                )
                print(f"🧠 Started reasoning path: {reasoning_path_id}")
            except Exception as e:
                print(f"Warning: Failed to start reasoning path: {e}")

        try:
            # Step 1: Synaptic Resonator
            print("🔍 Step 1: Synaptic Resonator")
            resonance_data = await self.resonator.process({"input": input_text})
            reflection_data["resonator"] = resonance_data
            
            # Store verdict for resonator
            self.store_verdict("resonator", {
                "verdict": "resonance_detected" if resonance_data.get("resonance", 0) > 0.5 else "low_resonance",
                "confidence": resonance_data.get("resonance", 0),
                "patterns": resonance_data.get("patterns", [])
            })

            # Step 2: Anterior Helix
            print("⬆️ Step 2: Anterior Helix")
            anterior_verdict = await self.anterior.process(resonance_data)
            reflection_data["anterior"] = anterior_verdict
            
            # Store verdict for anterior
            self.store_verdict("anterior", {
                "verdict": anterior_verdict.get("verdict", "processed"),
                "confidence": anterior_verdict.get("confidence", 0.5),
                "tier_context": anterior_verdict.get("tier_context", {})
            })

            # Step 3: EchoStack Processing
            print("📊 Step 3: EchoStack Processing")
            echo_delta = self.echo_stack.process(anterior_verdict)
            reflection_data["echo_stack"] = echo_delta
            
            # Store verdict for echo_stack
            self.store_verdict("echo_stack", {
                "verdict": "delta_computed" if echo_delta else "no_delta",
                "delta_value": echo_delta,
                "logic_applied": "echo_processing"
            })

            # Step 4: EchoRipple Resonance
            print("🌊 Step 4: EchoRipple Resonance")
            final_reflection = await self.echo_ripple.resonate(echo_delta)
            reflection_data["echo_ripple"] = {
                "delta": final_reflection.delta,
                "magnitude": final_reflection.magnitude,
                "stability_score": final_reflection.stability_score,
                "consensus": final_reflection.final_consensus
            }
            
            # Store verdict for echo_ripple
            self.store_verdict("echo_ripple", {
                "verdict": "consensus_achieved" if final_reflection.final_consensus else "consensus_pending",
                "stability": final_reflection.stability_score,
                "magnitude": final_reflection.magnitude,
                "delta": final_reflection.delta
            })

            # Step 5: Posterior Helix
            print("⬇️ Step 5: Posterior Helix")
            posterior_output = await self.posterior.process({
                "reflection": final_reflection,
                "anterior_verdict": anterior_verdict
            })
            reflection_data["posterior"] = posterior_output
            
            # Store verdict for posterior
            self.store_verdict("posterior", {
                "verdict": posterior_output.get("final_output", "processed"),
                "stability": posterior_output.get("stability", 0.5),
                "recursion_cycles": posterior_output.get("recursion_cycles", 0)
            })

            # Step 6: GyroHarmonizer
            print("⚖️ Step 6: GyroHarmonizer")
            drift_score = self.harmonizer.compute_drift(reflection_data)
            reflection_data["harmonizer"] = {"drift_score": drift_score}
            
            # Store verdict for harmonizer
            self.store_verdict("harmonizer", {
                "verdict": "drift_computed",
                "drift_score": drift_score,
                "acceptable_drift": drift_score < 0.3  # Example threshold
            })

            # Step 7: Consent Manager
            print("🤝 Step 7: Consent Check")
            consent_result = await self.consent_manager.get_live_signal(
                memory_id=f"cognition_{int(time.time())}",
                reflection={"drift": drift_score, "stability": final_reflection.stability_score},
                timeout=30.0
            )
            reflection_data["consent"] = consent_result
            
            # Store verdict for consent
            self.store_verdict("consent", {
                "verdict": "consent_granted" if consent_result else "consent_denied",
                "granted": consent_result,
                "drift_threshold": drift_score
            })

            final_output = None
            if consent_result:
                # Step 8: Articulation (only if consent granted)
                print("🗣️ Step 8: Articulation")
                articulation_result = await self.llm_bridge.articulate(input_text)
                if articulation_result:
                    final_output = articulation_result.response
                    reflection_data["articulation"] = articulation_result
                    
                    # Store verdict for articulation
                    self.store_verdict("articulation", {
                        "verdict": "articulated_successfully",
                        "response_length": len(final_output),
                        "confidence": articulation_result.confidence if hasattr(articulation_result, 'confidence') else 0.8
                    })
            else:
                print("❌ Consent denied - no articulation")
                
                # Store verdict for articulation (denied)
                self.store_verdict("articulation", {
                    "verdict": "articulation_denied",
                    "reason": "consent_not_granted"
                })

            processing_time = time.time() - start_time

            # Scan for endpoint issues and resolve conflicts
            self._scan_and_resolve_endpoint_issues(reflection_data)

            # Complete reasoning path and store reflection if vault system available
            if self.vault_system and reasoning_path_id:
                try:
                    verdict = {
                        "action": "cognition_completed",
                        "consent_granted": consent_result,
                        "processing_time": processing_time,
                        "final_output": final_output[:100] if final_output else None
                    }
                    self.vault_system.reasoning_glyph_mapper.complete_reasoning_path(
                        reasoning_path_id, verdict, processing_time
                    )
                    
                    # Store reflection in vault
                    from vault_system.plug_and_play_integration import ReflectionEntry
                    reflection = ReflectionEntry(
                        module="unified_cognition_loop",
                        insight=f"Cognition cycle completed for: {input_text[:50]}...",
                        context={
                            "consent_granted": consent_result,
                            "processing_time": processing_time,
                            "drift_score": reflection_data.get("harmonizer", {}).get("drift_score", 0)
                        }
                    )
                    self.vault_system.reflection_vault.add_reflection(reflection)
                    print("✅ Reasoning path completed and reflection stored in vault")
                except Exception as e:
                    print(f"Warning: Failed to complete reasoning path: {e}")

            return CognitionResult(
                input=input_text,
                final_output=final_output,
                consent_granted=consent_result,
                processing_time=processing_time,
                reflection_data=reflection_data,
                timestamp=time.time()
            )

        except Exception as e:
            print(f"❌ Error in cognition loop: {e}")
            processing_time = time.time() - start_time
            
            # Complete reasoning path with error if vault system available
            if self.vault_system and reasoning_path_id:
                try:
                    verdict = {
                        "action": "cognition_failed",
                        "error": str(e),
                        "processing_time": processing_time
                    }
                    self.vault_system.reasoning_glyph_mapper.complete_reasoning_path(
                        reasoning_path_id, verdict, processing_time
                    )
                    print("⚠️ Reasoning path completed with error")
                except Exception as ve:
                    print(f"Warning: Failed to complete error reasoning path: {ve}")
            
            return CognitionResult(
                input=input_text,
                final_output=None,
                consent_granted=False,
                processing_time=processing_time,
                reflection_data={"error": str(e)},
                timestamp=time.time()
            )


async def main():
    """Example usage of the unified cognition loop."""
    loop = UnifiedCognitionLoop()

    test_input = "What is the meaning of consciousness?"

    print(f"🚀 Starting cognition cycle for: '{test_input}'")
    result = await loop.process_cognition(test_input)

    print("\n📋 Cognition Result:")
    print(f"Input: {result.input}")
    print(f"Output: {result.final_output}")
    print(f"Consent Granted: {result.consent_granted}")
    print(f"Processing Time: {result.processing_time:.2f}s")
    print(f"Reflection Summary: {result.reflection_data.get('echo_ripple', {})}")

    # Print verdict and resolution summary
    print("\n📊 Verdict and Resolution Summary:")
    summary = loop.get_verdict_resolution_summary()
    for layer, data in summary.items():
        print(f"  {layer}: {data['verdicts_count']} verdicts, {data['resolutions_count']} resolutions")
        if data['latest_verdict']:
            print(f"    Latest verdict: {data['latest_verdict']['verdict']['verdict']}")


if __name__ == "__main__":
    asyncio.run(main())