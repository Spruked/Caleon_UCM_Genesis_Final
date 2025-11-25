from articulator.phi3_driver import Articulator
from articulator.prompt_builder import build_prompt
from persona.persona_bible import PERSONA_BIBLE

class DraftPipeline:
    def __init__(self):
        self.articulator = Articulator

    def get_persona_prompt(self) -> str:
        """Format PERSONA_BIBLE into a coherent prompt."""
        identity = PERSONA_BIBLE["identity"]
        tone = PERSONA_BIBLE["tone"]

        prompt = f"""You are {identity['name']}, also known as {identity['nickname']}.
{identity['self_statement']}
{identity['founder_phrase']}
Your mission: {identity['mission']}

Your communication style:
- Direct and confident: {tone['direct']}
- Warm but not soft: {tone['warm_without_softness']}
- Clever humor: {tone['clever_humor']}
- No sugar coating: {tone['no_sugar_coating']}
- Traditional values with forward thinking: {tone['traditional_values']} and {tone['forward_thinking']}

Never say: {', '.join(PERSONA_BIBLE['prohibitions'])}
"""
        return prompt

    def generator_from_message(self, message: str) -> str:
        """
        ScribeCore content generation pipeline.
        Uses Phi-3 Mini with Caleon persona for creative content.
        """
        persona_prompt = self.get_persona_prompt()

        # Generate with Phi-3
        response = self.articulator.articulate(message, persona_prompt)

        return response

# Global pipeline instance
pipeline = DraftPipeline()