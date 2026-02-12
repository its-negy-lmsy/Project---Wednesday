from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EmotionState:
    primary: str
    intensity: float


class EmotionTagger:
    """Lightweight emotion tagging stub.

    Replace with classifier model later.
    """

    POSITIVE = {"thanks", "love", "great", "awesome", "happy"}
    NEGATIVE = {"angry", "hate", "bad", "upset", "sad"}

    def detect(self, text: str) -> EmotionState:
        lowered = text.lower()
        if any(token in lowered for token in self.NEGATIVE):
            return EmotionState(primary="negative", intensity=0.8)
        if any(token in lowered for token in self.POSITIVE):
            return EmotionState(primary="positive", intensity=0.7)
        return EmotionState(primary="neutral", intensity=0.3)
