from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha1, sha256
from typing import Any, Deque, Dict, List

from .vector_store import SimpleVectorStore, VectorMatch, VectorStore


@dataclass(slots=True)
class MemoryRecord:
    memory_id: str
    text: str
    kind: str
    emotional_context: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class MemoryManager:
    def __init__(self, session_window: int = 20, vector_store: VectorStore | None = None) -> None:
        self.short_term: Deque[MemoryRecord] = deque(maxlen=session_window)
        self.long_term: Dict[str, MemoryRecord] = {}
        self.vector_store = vector_store or SimpleVectorStore()

    def remember(self, text: str, kind: str = "interaction", emotional_context: str = "neutral", **metadata: Any) -> MemoryRecord:
        memory_id = sha256(f"{text}|{kind}|{len(self.long_term)}".encode("utf-8")).hexdigest()[:16]
        record = MemoryRecord(
            memory_id=memory_id,
            text=text,
            kind=kind,
            emotional_context=emotional_context,
            metadata={k: str(v) for k, v in metadata.items()},
        )
        self.short_term.append(record)
        self.long_term[memory_id] = record
        self.vector_store.upsert(memory_id, _embed(text), _as_vector_metadata(record))
        return record

    def recall(self, query: str, top_k: int = 5) -> List[MemoryRecord]:
        matches: List[VectorMatch] = self.vector_store.query(_embed(query), top_k=top_k)
        return [self.long_term[m.key] for m in matches if m.key in self.long_term]


def _embed(text: str, dim: int = 64) -> List[float]:
    vector = [0.0] * dim
    tokens = [token.strip(".,!?;:\"'()[]{}").lower() for token in text.split()]
    for token in tokens:
        if not token:
            continue
        bucket = int(sha1(token.encode("utf-8")).hexdigest(), 16) % dim
        vector[bucket] += 1.0
    norm = sum(abs(value) for value in vector) or 1.0
    return [value / norm for value in vector]


def _as_vector_metadata(record: MemoryRecord) -> Dict[str, str]:
    data = {"kind": record.kind, "emotional_context": record.emotional_context, "created_at": record.created_at}
    data.update({k: str(v) for k, v in record.metadata.items()})
    return data
