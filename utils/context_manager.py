from persona.persona_router import PersonaRouter
from generative.router import GenerativeRouter

class BubbleContext:

    @staticmethod
    def route(message: str) -> str:
        """
        Intelligence routing:
        - Short/simple → Scripted Caleon
        - Complex/creative → Generative Caleon
        """
        simple_triggers = [
            "hi", "hello", "hey", "menu", "help", "save",
            "ok", "thanks", "thank you"
        ]

        text = message.lower().strip()

        if any(x in text for x in simple_triggers):
            return "scripted"
        return "generative"


    @staticmethod
    def scripted(message: str):
        """
        Use CALI Scripts for consistent personality responses.
        """
        return PersonaRouter.scripted("greetings", "generic_welcome")


    @staticmethod
    async def generative(message: str, session_id: str = None, user: str = None):
        """
        Route to UCM reasoning engine with intent analysis and planning.
        """
        return await GenerativeRouter.handle(message, session_id, user)


    @staticmethod
    def stream_placeholder(message: str):
        """
        Streaming placeholder; real stream comes in Phase 3.
        """
        return {
            "type": "stream",
            "reply": f"[Streaming not yet enabled] {message}"
        }