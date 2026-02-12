from __future__ import annotations

from pathlib import Path

from .conversation import ConversationEngine
from .memory import MemoryManager
from .personality import PersonalityStore


def build_engine(base_path: str = ".") -> ConversationEngine:
    personality_path = Path(base_path) / "personalities" / "wednesday.json"
    store = PersonalityStore(personality_path)
    profile = store.load()
    memory = MemoryManager(session_window=30)
    return ConversationEngine(personality=profile, memory=memory)
