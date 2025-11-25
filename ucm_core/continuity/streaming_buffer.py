class StreamingMemoryBuffer:
    """
    Stores rolling context during an active stream.
    This is NOT long-term vault memory.
    """
    def __init__(self):
        self.lines = []
        self.max_items = 20

    def add(self, text: str):
        text = text.strip()
        if text:
            self.lines.append(text)
            self.lines = self.lines[-self.max_items:]

    def get(self):
        return "\n".join(self.lines)