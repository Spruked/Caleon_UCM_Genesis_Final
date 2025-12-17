from utils.phi3_client import phi3_client
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
    Streaming response using Phi-3 via Ollama with real token streaming.
    """
    persona_prompt = get_persona_prompt()
    full_prompt = f"{persona_prompt}\n\nUser: {message}\n\nCaleon:"

    # Use real streaming from Ollama
    async for token in phi3_client.stream_generate(full_prompt, max_tokens=300, temperature=0.7):
        yield f"data: {token}\n\n"
        await asyncio.sleep(0.01)  # Small delay for smooth streaming

    yield "data: [DONE]\n\n"