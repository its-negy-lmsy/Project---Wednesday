# Wednesday API (Artificial Personality Intelligence)

Wednesday is a modular foundation for building a persistent, emotionally-aware, goal-driven AI companion.
This repository provides a **production-minded architecture skeleton** you can extend into a full autonomous system.

## Vision

Build an AI that can:
- maintain a consistent, evolving personality,
- remember interactions and retrieve relevant context,
- plan and execute multi-step goals,
- align responses with emotional context,
- integrate with external tools safely,
- eventually control broader software/OS environments.

## Repository structure

```text
.
├── configs/                  # Runtime settings
├── memory/                   # Persistent memory artifacts (runtime)
├── personalities/            # Personality profiles persisted as JSON
├── src/
│   └── wednesday/
│       ├── app.py            # Wiring/bootstrap for conversation engine
│       ├── conversation.py   # Conversational layer with memory + tone
│       ├── emotion.py        # Emotion tagging module
│       ├── goals.py          # Goal planning and service execution stubs
│       ├── memory.py         # Short-term + long-term memory manager
│       ├── personality.py    # Personality model + persistence
│       └── vector_store.py   # Vector store abstraction + local implementation
└── tests/                    # Core module tests
```

## Core components

### 1) Personality modeling
- `PersonalityProfile` captures:
  - core traits,
  - social boundaries for new/trusted/conflict interactions,
  - speaking style,
  - dynamic reinforcement state.
- `PersonalityStore` persists profile state and supports reinforcement signals.

### 2) Long-term memory
- `MemoryManager` maintains:
  - short-term session memory (`deque`, bounded window),
  - long-term indexed memory records.
- `VectorStore` protocol allows plugging in Chroma, Weaviate, Milvus, etc.
- `SimpleVectorStore` is included for local development/tests.
- Retrieval pipeline:
  1. text embedding,
  2. vector similarity search,
  3. inject top memories into conversation context.

### 3) Goal-driven autonomy
- `GoalPlanner` transforms high-level objectives into a sequenced plan.
- `TaskExecutor` routes actions to registered services (memory lookup, knowledge, scheduling, etc.).
- Designed for extension into closed-loop evaluate/refine execution.

### 4) Natural conversational layer
- `ConversationEngine` combines:
  - personality style,
  - emotion detection,
  - recalled memory context.
- Output includes tone selection (`balanced`, `empathetic`, `enthusiastic`) and persistent memory writes.

### 5) Tool integration
- Tool invocation should occur behind `TaskExecutor` service contracts.
- Suggested pattern:
  - strict schemas for tool input/output,
  - audit logs for tool calls,
  - policy checks before side-effectful actions.

### 6) Personality reinforcement & emotional context
- `EmotionTagger` tags interaction polarity and intensity.
- Reinforcement hooks update personality dynamic state based on interaction outcomes.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## Running tests

```bash
pytest
```

## Basic usage

```python
from wednesday.app import build_engine

engine = build_engine(base_path='.')
print(engine.reply("Hi Wednesday, I feel upset today"))
print(engine.reply("Do you remember what I said?"))
```

## How to train/fine-tune modules (roadmap)

### Personality behavior training
- Start with rule-based style constraints (already scaffolded).
- Add preference learning from explicit feedback signals.
- For advanced conversational style learning, curate consent-safe dialogue datasets and fine-tune adapters.

### Emotional modeling
- Replace keyword-based `EmotionTagger` with a transformer classifier.
- Track valence/arousal over time and use smoothing to avoid abrupt mood swings.

### Memory quality improvements
- Swap `_embed()` with production embeddings (e.g., sentence-transformers).
- Add memory scoring (importance, novelty, recency).
- Add memory consolidation and summarization jobs.

### Autonomy loop
- Add planner/executor/evaluator loop with bounded retries and reflection summaries.
- Persist plan state and tool traces for observability.

## Extension guide

1. **Vector DB integration**
   - Implement `VectorStore` adapter for Chroma/Milvus/Weaviate.
2. **LLM backend integration**
   - Replace template response logic with LLM calls in `ConversationEngine`.
3. **Real-time UI**
   - Add WebSocket chat server + frontend.
4. **OS/tool control**
   - Expose controlled tool APIs (filesystem, browser automation, calendar).
   - enforce permissions and human-in-the-loop gating for risky operations.
5. **Vtuber/avatar interface**
   - Add speech-to-text, text-to-speech, and avatar animation pipeline.

## Safety notes

- Keep explicit boundaries for autonomy.
- Require approvals for high-risk actions.
- Encrypt sensitive memory and support data deletion/export.

---

This codebase is intentionally modular so Wednesday can evolve from a conversational assistant into an autonomous long-term companion intelligence.
