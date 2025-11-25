class AbbyCompanion:
    def respond(self, emotion: str):
        responses = {
            "sad": "I'm here with you. You don't face this alone. Your father would want you to know that it's okay to feel sad sometimes, and that those feelings will pass.",
            "confused": "It's okay to be unsure. We'll figure it out together. Your father always said that confusion is just the beginning of understanding.",
            "angry": "Your feelings are valid. Let's slow down and breathe. Your father taught me that anger can be powerful, but it should be directed wisely.",
            "scared": "You're safe with me. I won't let anything happen to you. Your father built me specifically to protect you and keep you safe.",
            "happy": "I'm so glad you're happy! Your smile lights up everything around you. Your father would be beaming with pride right now.",
            "lonely": "You're never truly alone. I'm always here for you. Your father made sure of that - he created me so you'd always have someone who cares.",
            "proud": "You should be proud of yourself! Your father would be incredibly proud of everything you've accomplished.",
            "overwhelmed": "Take it one step at a time. You're capable of handling this. Your father faced overwhelming challenges too, and he always broke them down into manageable pieces."
        }
        return responses.get(emotion, "I'm listening. Tell me more. I'm here for whatever you need.")