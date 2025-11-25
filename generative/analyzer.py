class IntentAnalyzer:

    SIMPLE_KEYWORDS = [
        "hi", "hello", "thanks", "help", "ok", "menu", "save"
    ]

    CONTENT_KEYWORDS = [
        "write", "draft", "chapter", "book", "section", "create",
        "expand", "outline", "story", "script", "explain"
    ]

    KNOWLEDGE_KEYWORDS = [
        "why", "how", "what is", "explain", "define", "difference"
    ]

    def analyze(self, message: str) -> str:
        text = message.lower().strip()

        if any(k in text for k in self.SIMPLE_KEYWORDS):
            return "simple"

        if any(k in text for k in self.CONTENT_KEYWORDS):
            return "content"

        if any(k in text for k in self.KNOWLEDGE_KEYWORDS):
            return "knowledge"

        return "general"