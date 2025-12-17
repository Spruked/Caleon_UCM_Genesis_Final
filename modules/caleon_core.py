"""
CaleonCore: Orchestrator for the Caleon 2.0 Core Reasoning System
Implements the multi-layer pyramid, micro-resonator grid, and core module logic as described.
"""
from modules.Synaptic_Resonator import SynapticResonator
from modules.anterior_pituitary_helix import AnteriorPituitaryHelix
from modules.posterior_pituitary_helix import PosteriorPituitaryHelix
from modules.echo_stack import EchoStack
from modules.gyroscopic_harmonizer import GyroscopicHarmonizer
import time
import logging

logger = logging.getLogger(__name__)

# Optional voice integration - gracefully degrade if unavailable
VOICE_AVAILABLE = False
try:
    from voice_processor import voice_processor
    VOICE_AVAILABLE = True
    logger.info("Voice systems integrated: Cochlear Processor + Phonatory Output")
except ImportError as e:
    logger.warning(f"Voice systems not available: {e}")

class CaleonCore:
    def __init__(self):
        # Core cognitive modules
        self.synaptic_resonator = SynapticResonator(core_callback=lambda x: x)
        self.anterior_helix = AnteriorPituitaryHelix()
        self.posterior_helix = PosteriorPituitaryHelix()
        self.echo_stack = EchoStack()
        self.echo_ripple = EchoStack(trailing_ms=20, randomize_logic=True)
        self.gyro_harmonizer = GyroscopicHarmonizer()
        
        # Voice integration status
        self.voice_enabled = VOICE_AVAILABLE

    def process(self, input_data):
        """
        Process input through full cognitive pipeline.
        Supports text input (default) and audio input (if voice systems available).
        """
        # STAGE 1: Input Processing
        # Check if input is audio or text
        raw_input = input_data
        if isinstance(input_data, dict) and input_data.get("audio_file"):
            # Audio input - use Cochlear Processor if available
            if self.voice_enabled:
                try:
                    transcribed = voice_processor.speech_to_text(input_data["audio_file"])
                    if transcribed:
                        raw_input = {"content": transcribed, **input_data}
                        logger.info(f"Cochlear processed audio: {transcribed[:50]}...")
                except Exception as e:
                    logger.error(f"Cochlear processing failed: {e}")
        
        # STAGE 2: Normalize input for Synaptic Resonator
        normalized = {
            "signal": raw_input,
            "timestamp": time.time(),
            "pulse": self.synaptic_resonator.next_pulse(),
            "source": "UCM"
        }
        pyramid_output = self.synaptic_resonator.pyramid_distill(normalized)

        # STAGE 3: Dual Helix Processing (biological timing enforced)
        anterior_result = self.anterior_helix.process(pyramid_output)
        
        # Posterior Helix fires 20ms later
        time.sleep(0.020)
        posterior_result = self.posterior_helix.process(pyramid_output)

        # STAGE 4: Echo Processing
        echo_stack_result = self.echo_stack.process(pyramid_output)
        echo_ripple_result = self.echo_ripple.process(pyramid_output)

        # STAGE 5: Harmonization
        final_decision = self.gyro_harmonizer.harmonize_all(
            anterior_result, posterior_result, echo_stack_result, echo_ripple_result
        )

        # STAGE 6: Vault Storage
        self.gyro_harmonizer.vault.store_cycle({
            "input": raw_input,
            "pyramid": pyramid_output,
            "anterior": anterior_result,
            "posterior": posterior_result,
            "echo": echo_stack_result,
            "ripple": echo_ripple_result,
            "final": final_decision,
        })

        # STAGE 7: Output Processing (voice if enabled and requested)
        if self.voice_enabled and isinstance(input_data, dict) and input_data.get("voice_output"):
            try:
                # Extract text response from final decision
                response_text = str(final_decision.get("final_verdict", "Processing complete"))
                voice_processor.text_to_speech(response_text)
                logger.info("Phonatory output generated")
            except Exception as e:
                logger.error(f"Phonatory output failed: {e}")

        return final_decision