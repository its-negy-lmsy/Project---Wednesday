from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .emotion import EmotionTagger
from .memory import MemoryManager
from .personality import PersonalityProfile


@dataclass(slots=True)
class ConversationTurn:
    user_message: str
    assistant_message: str


class ConversationEngine:
    def __init__(self, personality: PersonalityProfile, memory: MemoryManager, emotion_tagger: EmotionTagger | None = None) -> None:
        self.personality = personality
        self.memory = memory
        self.emotion_tagger = emotion_tagger or EmotionTagger()

    def reply(self, user_message: str) -> str:
        emotion = self.emotion_tagger.detect(user_message)
        self.memory.remember(user_message, kind="user", emotional_context=emotion.primary)
        recalled = self.memory.recall(user_message, top_k=2)
        context = "; ".join(record.text for record in recalled if record.text != user_message)

        tone = self._tone_from_emotion(emotion.primary)
        response = (
            f"[{self.personality.name} | tone={tone}] "
            f"I hear you. {self._style_prompt()}"
            + (f" I remember related context: {context}." if context else "")
        )
        self.memory.remember(response, kind="assistant", emotional_context=tone)
        return response

    def _tone_from_emotion(self, emotion: str) -> str:
        if emotion == "negative":
            return "empathetic"
        if emotion == "positive":
            return "enthusiastic"
        return "balanced"

    def _style_prompt(self) -> str:
        traits: List[str] = self.personality.core_traits[:2]
        return f"I'll respond as {', '.join(traits)} and {self.personality.speaking_style}."
