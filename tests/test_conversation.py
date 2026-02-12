from wednesday.conversation import ConversationEngine
from wednesday.memory import MemoryManager
from wednesday.personality import PersonalityProfile


def test_conversation_maintains_personality_signature() -> None:
    engine = ConversationEngine(personality=PersonalityProfile(), memory=MemoryManager())

    response = engine.reply("Hi, I am new here")

    assert "[Wednesday" in response
    assert "curious" in response or "calm" in response


def test_conversation_uses_emotional_tone() -> None:
    engine = ConversationEngine(personality=PersonalityProfile(), memory=MemoryManager())

    negative_response = engine.reply("I feel sad and upset")
    positive_response = engine.reply("I am happy and awesome")

    assert "empathetic" in negative_response
    assert "enthusiastic" in positive_response
