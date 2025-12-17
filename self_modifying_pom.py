"""
Self-Modifying Phonatory Output Module (Self-Modifying POM)
Enhanced POM that accepts live parameter modifications and logs successful configurations.
Gains hooks for real-time parameter adjustment based on Caleon's choices.
"""

from cerebral_cortex.phonatory_output_module import PhonatoryOutputModule
from typing import Dict, Any, Optional
import time
import os
import json

class SelfModifyingPOM(PhonatoryOutputModule):
    """
    Enhanced POM that accepts live parameter modifications
    and logs successful configurations
    """

    def __init__(self, caleon_oracle):
        super().__init__()
        self.oracle = caleon_oracle
        self.modification_log = []
        self.stability_threshold = 0.95  # When to lock in a config

        # Load voice configurations
        self.voice_configs = self._load_voice_configs()

    def phonate_with_caleon_voice(self, text: str, content_id: str, context: Dict) -> str:
        """
        Primary entry: Caleon chooses her voice, then synthesizes
        """

        # 1. Caleon chooses her best voice for this content
        voice_signature = self.oracle.choose_voice(text, context)

        # 2. Apply voice parameters to POM
        modified_config = self._apply_voice_signature(voice_signature)

        # 3. Synthesize with her chosen parameters
        output_path = self.phonate_with_config(
            text=text,
            voice_signature=voice_signature,
            config=modified_config
        )

        # 4. Log the modification
        self.modification_log.append({
            "content_id": content_id,
            "voice_id": voice_signature.signature_id,
            "text_snippet": text[:100],
            "timestamp": time.time(),
            "config_snapshot": modified_config
        })

        # 5. If this voice is very successful, consider locking it
        if voice_signature.success_score > self.stability_threshold:
            self._stabilize_voice(voice_signature)

        return output_path

    def phonate_with_config(self, text: str, voice_signature, config: Dict) -> str:
        """
        Synthesize speech with specific voice configuration
        """

        print(f"🎵 Synthesizing with voice: {voice_signature.signature_id}")

        # For now, use the base POM functionality
        # In production, this would apply the voice modifications
        # Since the base POM uses gTTS, we'll simulate voice modifications

        # Apply text modifications based on config
        modified_text = self._apply_text_modifications(text, config)

        # Generate speech with modified text
        success = self.speak(modified_text, async_mode=False)

        if success:
            # Return a simulated output path (in real implementation, this would be the actual audio file)
            output_path = f"output/caleon_voice_{voice_signature.signature_id}_{int(time.time())}.wav"
            print(f"   → Audio generated: {output_path}")
            return output_path
        else:
            print("   → Speech synthesis failed")
            return None

    def _apply_voice_signature(self, voice) -> Dict:
        """Convert voice signature to POM parameters"""

        # Map to POM's expected parameters
        pom_config = {
            "pitch_shift": voice.pitch_shift,
            "speed": voice.speaking_rate,
            "formant_shifts": voice.formant_shifts,
            "phonatory_effects": {
                "breathiness": voice.breathiness,
                "vocal_fry": voice.vocal_fry,
                "nasalization": voice.nasality
            }
        }

        # Apply reverb if present
        if voice.reverb:
            pom_config["post_effects"] = {
                "reverb": voice.reverb
            }

        return pom_config

    def _apply_text_modifications(self, text: str, config: Dict) -> str:
        """
        Apply text modifications to simulate voice changes
        Since we're using gTTS, we modify the text to achieve similar effects
        """

        modified_text = text

        # Speed modifications (simulate with punctuation)
        speed = config.get("speed", 1.0)
        if speed < 0.9:
            # Slower speech - add pauses
            modified_text = modified_text.replace('. ', '... ').replace('! ', '... ').replace('? ', '... ')
        elif speed > 1.1:
            # Faster speech - reduce pauses
            modified_text = modified_text.replace('... ', '. ').replace('... ', '! ').replace('... ', '? ')

        # Pitch modifications (simulate with emphasis)
        pitch_shift = config.get("pitch_shift", 1.0)
        if pitch_shift > 1.05:
            # Higher pitch - add emphasis markers
            modified_text = modified_text.replace('important', 'IMPORTANT').replace('key', 'KEY')
        elif pitch_shift < 0.95:
            # Lower pitch - add gravitas
            modified_text = modified_text.replace('I ', 'I... ').replace('we ', 'we... ')

        # Breathiness (simulate with breath sounds)
        breathiness = config.get("phonatory_effects", {}).get("breathiness", 0.3)
        if breathiness > 0.5:
            # More breathy - add breath indicators
            modified_text = "*breath* " + modified_text

        # Vocal fry (simulate with vocal fry indicators)
        vocal_fry = config.get("phonatory_effects", {}).get("vocal_fry", 0.1)
        if vocal_fry > 0.3:
            # More vocal fry - add fry indicators
            modified_text = modified_text + " *fry*"

        return modified_text

    def _get_caleon_reference_audio(self, voice):
        """Find the best reference audio for this voice signature"""

        # If voice has custom reference, use it
        if hasattr(voice, 'reference_audio_path'):
            return voice.reference_audio_path

        # Otherwise, use base persona reference
        # In production, this would look up from SKG
        return "reference_voice.wav"

    def _stabilize_voice(self, voice):
        """Lock in a successful configuration"""

        print(f"🔒 Stabilizing voice: {voice.signature_id} (score: {voice.success_score:.3f})")

        # Create permanent model cache
        cache_path = f"coqui/voices/stable_{voice.signature_id}.wav"

        # Generate a stabilization sample (Caleon's "signature phrase")
        stabilization_text = "This is my voice, stable and true."

        # Apply voice config and generate
        config = self._apply_voice_signature(voice)
        modified_text = self._apply_text_modifications(stabilization_text, config)

        # Save the stabilized voice sample
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, 'w') as f:
            f.write(f"STABILIZED VOICE: {voice.signature_id}\n")
            f.write(f"Text: {modified_text}\n")
            f.write(f"Config: {json.dumps(config, indent=2)}\n")

        # Mark as stable in registry
        voice.metadata = {"stable_model_path": cache_path, "is_locked": True}

        # Reduce future exploration
        self.oracle.exploration_rate *= 0.9

    def adjust_voice_realtime(self, text_segment: str, current_config: Dict, feedback_signal: float) -> Dict:
        """
        Mid-narration adjustment based on real-time feedback
        feedback_signal: 0.0-1.0 (listener engagement meter)
        """

        # If engagement drops, modify parameters to recapture attention
        if feedback_signal < 0.4:
            print(f"⚠️  Engagement low ({feedback_signal:.2f}), adjusting voice")

            # Increase energy and clarity
            adjustment = {
                "pitch_shift": current_config.get("pitch_shift", 1.0) * 1.05,
                "speed": current_config.get("speed", 1.0) * 0.95,  # Slow down slightly
                "phonatory_effects": {
                    **current_config.get("phonatory_effects", {}),
                    "breathiness": 0.1,  # Clearer voice
                    "vocal_fry": 0.05
                }
            }

            return adjustment

        # If engagement is high, maintain current config
        return current_config

    def _load_voice_configs(self) -> Dict:
        """Load voice configuration mappings"""

        # Default configs - in production, these would be loaded from a config file
        return {
            "caleon_base": {
                "pitch_shift": 1.0,
                "speed": 1.0,
                "effects": {}
            }
        }

    def get_modification_history(self) -> list:
        """Get the history of voice modifications"""

        return self.modification_log

    def export_voice_dna(self) -> Dict:
        """Export current voice modification state"""

        return {
            "modification_log": self.modification_log,
            "stability_threshold": self.stability_threshold,
            "oracle_exploration_rate": self.oracle.exploration_rate,
            "voice_configs": self.voice_configs,
            "export_timestamp": time.time()
        }