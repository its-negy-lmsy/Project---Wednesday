from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass(slots=True)
class PersonalityProfile:
    name: str = "Wednesday"
    core_traits: List[str] = field(default_factory=lambda: ["curious", "calm", "supportive"])
    social_boundaries: Dict[str, str] = field(
        default_factory=lambda: {
            "new_people": "polite, gentle, and reserved",
            "trusted_people": "open, warm, and playful",
            "conflict": "firm, reflective, and de-escalating",
        }
    )
    speaking_style: str = "concise, emotionally-aware, and respectful"
    dynamic_state: Dict[str, str] = field(default_factory=lambda: {"trust_level": "medium", "energy": "stable"})


class PersonalityStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> PersonalityProfile:
        if not self.path.exists():
            profile = PersonalityProfile()
            self.save(profile)
            return profile
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return PersonalityProfile(**data)

    def save(self, profile: PersonalityProfile) -> None:
        self.path.write_text(json.dumps(asdict(profile), indent=2), encoding="utf-8")

    def reinforce(self, profile: PersonalityProfile, signal: str) -> PersonalityProfile:
        if signal == "positive_interaction":
            profile.dynamic_state["trust_level"] = "high"
        elif signal == "stress":
            profile.dynamic_state["energy"] = "low"
            profile.speaking_style = "soft, reassuring, and minimal"
        self.save(profile)
        return profile
