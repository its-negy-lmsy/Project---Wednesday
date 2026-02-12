from pathlib import Path

from wednesday.personality import PersonalityProfile, PersonalityStore


def test_personality_persistence_round_trip(tmp_path: Path) -> None:
    store = PersonalityStore(tmp_path / "wednesday.json")
    profile = PersonalityProfile(name="Wednesday", core_traits=["empathetic"])
    store.save(profile)

    loaded = store.load()
    assert loaded.name == "Wednesday"
    assert loaded.core_traits == ["empathetic"]


def test_personality_reinforcement_updates_state(tmp_path: Path) -> None:
    store = PersonalityStore(tmp_path / "wednesday.json")
    profile = store.load()

    updated = store.reinforce(profile, "positive_interaction")
    assert updated.dynamic_state["trust_level"] == "high"
