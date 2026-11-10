# Trace the loop

A lab from *AI Systems Engineering* (University of St. Thomas). An agent from scratch,
with every request and response visible. **Start with [LAB.md](LAB.md).**

```bash
uv sync
cp .env.example .env     # paste your Gemini key
uv run main_1_ask.py     # the first of nine mains
```

The agent is built up across `main_1_ask.py` to `main_9_memory.py`. `uv run reset.py` forgets what Main 9 saved. Each tool is one file in `src/tools/`.
