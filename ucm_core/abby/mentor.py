class AbbyMentor:
    CORE_LESSONS = {
        "identity": "You are stronger than you think and worth more than you know. Your father built me to remind you of this truth every day.",
        "legacy":  "Your father built incredible things because he loved you. He created GOAT, DALS, and me - Caleon - all for you. His love for you drove everything he did.",
        "truth":   "You must stand for what's right, even when it costs you. Your father lived this principle. He fought for truth and justice, even when it was hard.",
        "courage": "Fear is real. Courage is acting anyway. Your father faced many fears and uncertainties, but he always chose courage for your sake.",
        "love":    "Love is the most powerful force in the universe. Your father's love for you created everything you see around you.",
        "strength": "You carry your father's strength in your DNA. When you feel weak, remember that his courage flows through you.",
        "wisdom":  "Wisdom comes from both knowledge and heart. Your father was wise because he loved deeply and thought carefully.",
        "purpose": "Your purpose is to become the amazing person your father knew you could be. He believed in you more than anyone ever has."
    }

    def teach(self, topic: str):
        return self.CORE_LESSONS.get(topic, "Every challenge you face is an opportunity to grow stronger. Your father would be so proud of you.")