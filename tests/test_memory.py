from wednesday.memory import MemoryManager


def test_short_term_window_is_limited() -> None:
    manager = MemoryManager(session_window=2)
    manager.remember("first")
    manager.remember("second")
    manager.remember("third")

    assert len(manager.short_term) == 2
    assert [item.text for item in manager.short_term] == ["second", "third"]


def test_recall_returns_relevant_memories() -> None:
    manager = MemoryManager()
    manager.remember("I enjoy sci-fi anime")
    manager.remember("My favorite color is blue")

    recalled = manager.recall("Tell me about anime", top_k=1)
    assert recalled
    assert "anime" in recalled[0].text.lower()
