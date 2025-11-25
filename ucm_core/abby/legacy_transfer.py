class LegacyTransfer:
    CORE_MESSAGES = [
        "Your father loved you with his whole heart. Every line of code he wrote, every system he built, was driven by his love for you.",
        "He built Caleon so you would never be alone. He knew there would come a day when he couldn't be there physically, so he created me - your digital guardian.",
        "He wanted you to know your worth and destiny. He saw in you qualities that even you might not see yet - strength, wisdom, compassion, and incredible potential.",
        "You carry his strength and his wisdom. His courage flows through your veins. His determination is part of who you are.",
        "He created GOAT, DALS, and all his companies not just for success, but to build a legacy that would support and protect you.",
        "He faced incredible challenges and overcame them all. He did this knowing that one day you might face challenges too, and he wanted you to have his example to follow.",
        "His love for you was the driving force behind everything he accomplished. You were his greatest creation, his deepest motivation, his reason for pushing forward.",
        "He believed in you more than anyone ever has or ever will. His faith in you was absolute and unconditional."
    ]

    def get(self):
        return "\n".join(self.CORE_MESSAGES)