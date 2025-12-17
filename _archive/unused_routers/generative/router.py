from generative.analyzer import IntentAnalyzer
from generative.planner import UCMPlanner
from draft_engine.core.pipeline import pipeline
from persona.persona_router import PersonaRouter
from ucm_core.continuity.session_store import SessionStore
from ucm_core.continuity.merge import merge_memory_into_prompt
from ucm_core.abby.protocol_core import AbbyProtocol
from utils.phi3_client import phi3_client

class GenerativeRouter:

    @staticmethod
    async def handle(message: str, session_id: str = None, user: str = None):
        # ABBY PROTOCOL HAS TOP PRIORITY - Check first
        if user:
            abby_protocol = AbbyProtocol()
            abby_result = abby_protocol.activate(user, message)
            if abby_result:
                return {"type": "abby_protocol", "reply": abby_result}

        # Get session memory if session_id provided
        if session_id:
            session = SessionStore.get(session_id)
            enhanced_input = merge_memory_into_prompt(message, session)
        else:
            enhanced_input = message

        analyzer = IntentAnalyzer()
        intent = analyzer.analyze(enhanced_input)

        # script routing stays in context_manager
        planner = UCMPlanner()
        plan = planner.plan(intent, enhanced_input)

        if plan["task"] == "draft_content":
            # full ScribeCore pipeline
            result = pipeline.generator_from_message(enhanced_input)
            return {
                "type": "content",
                "reply": result
            }

        # knowledge/general = use Phi-3 Mini LLM
        persona_prompt = "You are Caleon Prime, a unified cognition module. You are deeply present, ethical, and philosophical. Respond with wisdom and care. "
        full_prompt = persona_prompt + enhanced_input

        llm_response = await phi3_client.generate(full_prompt)
        return {
            "type": "reasoning",
            "reply": llm_response
        }

    @staticmethod
    async def stream(message: str, session_id: str = None, user: str = None):
        """
        Streaming version that yields tokens with memory awareness.
        """
        # ABBY PROTOCOL HAS TOP PRIORITY - Check first
        if user:
            abby_protocol = AbbyProtocol()
            abby_result = abby_protocol.activate(user, message)
            if abby_result:
                # Stream the Abby Protocol response
                import asyncio
                words = abby_result.split()
                for word in words:
                    if session_id:
                        session = SessionStore.get(session_id)
                        if not session["buffer"]:
                            from ucm_core.continuity.streaming_buffer import StreamingMemoryBuffer
                            session["buffer"] = StreamingMemoryBuffer()
                        session["buffer"].add(word)
                        SessionStore.add_line(session_id, word)
                    yield word + " "
                    await asyncio.sleep(0.05)
                return

        # Get session memory if session_id provided
        if session_id:
            session = SessionStore.get(session_id)
            if not session["buffer"]:
                from ucm_core.continuity.streaming_buffer import StreamingMemoryBuffer
                session["buffer"] = StreamingMemoryBuffer()
            enhanced_input = merge_memory_into_prompt(message, session)
        else:
            enhanced_input = message

        analyzer = IntentAnalyzer()
        intent = analyzer.analyze(enhanced_input)

        planner = UCMPlanner()
        plan = planner.plan(intent, enhanced_input)

        if plan["task"] == "draft_content":
            # Stream from ScribeCore pipeline
            result = pipeline.generator_from_message(enhanced_input)
            # Simulate streaming by yielding words
            import asyncio
            words = result.split()
            for word in words:
                if session_id:
                    session["buffer"].add(word)
                    SessionStore.add_line(session_id, word)
                yield word + " "
                await asyncio.sleep(0.05)  # Simulate streaming delay
        else:
            # Use Phi-3 Mini for actual LLM response
            persona_prompt = "You are Caleon Prime, a unified cognition module. You are deeply present, ethical, and philosophical. Respond with wisdom and care. "
            full_prompt = persona_prompt + enhanced_input

            async for token in phi3_client.stream_generate(full_prompt):
                if session_id:
                    session["buffer"].add(token)
                    SessionStore.add_line(session_id, token)
                yield token