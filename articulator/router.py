from articulator.phi3_driver import Articulator
from articulator.prompt_builder import build_prompt
from persona.persona_bible import PERSONA_BIBLE
import asyncio

def get_persona_prompt() -> str:
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

async def stream_response(message: str):
    """
    Streaming response using Phi-3 with simulated token streaming.
    """
    persona_prompt = get_persona_prompt()

    # Generate full response
    full_response = Articulator.articulate(message, persona_prompt)

    # Simulate streaming by yielding chunks
    words = full_response.split()
    for i, word in enumerate(words):
        yield f"data: {word}{' ' if i < len(words)-1 else ''}\n\n"
        await asyncio.sleep(0.05)  # Small delay to simulate streaming

    yield "data: [DONE]\n\n"