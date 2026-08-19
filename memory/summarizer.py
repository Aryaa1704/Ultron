class MemorySummarizer:
    def summarize(self, texts: list[str], max_items: int = 5) -> str:
        if not texts:
            return "No memory items available."
        selected = texts[:max_items]
        bullet_points = "\n".join(f"- {text}" for text in selected)
        return f"Conversation memory summary:\n{bullet_points}"
