from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(slots=True)
class PlanStep:
    id: int
    description: str
    status: str = "pending"


class GoalPlanner:
    def plan(self, objective: str) -> List[PlanStep]:
        chunks = [c.strip() for c in objective.split(".") if c.strip()]
        if not chunks:
            chunks = [objective]
        return [PlanStep(id=index + 1, description=chunk) for index, chunk in enumerate(chunks)]


class TaskExecutor:
    def __init__(self) -> None:
        self.services: Dict[str, Callable[[str], str]] = {}

    def register(self, name: str, func: Callable[[str], str]) -> None:
        self.services[name] = func

    def execute(self, service: str, payload: str) -> str:
        if service not in self.services:
            raise KeyError(f"Unknown service: {service}")
        return self.services[service](payload)
