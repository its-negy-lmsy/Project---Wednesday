from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Dict, Iterable, List, Protocol, Tuple


@dataclass(slots=True)
class VectorMatch:
    key: str
    score: float
    metadata: Dict[str, str]


class VectorStore(Protocol):
    def upsert(self, key: str, vector: List[float], metadata: Dict[str, str]) -> None:
        ...

    def query(self, vector: List[float], top_k: int = 5) -> List[VectorMatch]:
        ...


class SimpleVectorStore:
    """A small in-process vector index.

    This serves as a default implementation for development and tests.
    In production, replace with Chroma/Milvus/Weaviate adapters implementing `VectorStore`.
    """

    def __init__(self) -> None:
        self._vectors: Dict[str, Tuple[List[float], Dict[str, str]]] = {}

    def upsert(self, key: str, vector: List[float], metadata: Dict[str, str]) -> None:
        self._vectors[key] = (vector, metadata)

    def query(self, vector: List[float], top_k: int = 5) -> List[VectorMatch]:
        scored: List[VectorMatch] = []
        for key, (candidate, metadata) in self._vectors.items():
            scored.append(VectorMatch(key=key, score=_cosine(vector, candidate), metadata=metadata))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]


def _cosine(a: Iterable[float], b: Iterable[float]) -> float:
    a_list = list(a)
    b_list = list(b)
    if len(a_list) != len(b_list) or not a_list:
        return 0.0
    dot = sum(x * y for x, y in zip(a_list, b_list))
    norm_a = sqrt(sum(x * x for x in a_list))
    norm_b = sqrt(sum(y * y for y in b_list))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
