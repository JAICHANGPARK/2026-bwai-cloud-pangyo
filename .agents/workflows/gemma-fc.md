---
name: gemma-fc
description: Generate Gemma 4 Function Calling Code
---

1. Read the rules in [gemma4_fc.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_fc.md).
2. Write or update the Python script at `hands-on/function_calling.py` using `httpx` and `asyncio` to implement function calling.
3. Define a `get_current_weather(location)` function that calls the `wttr.in` JSON API (`https://wttr.in/{location}?format=j1`) to fetch real weather data.
4. Step 1 (Tool Assessment) should be non-streaming (`stream=False`), and Step 2 (Final Response) should be streaming (`stream=True`).
5. Handle Ollama-native and OpenAI-compatible tool response formats.
6. Implement a terminal interactive loop (`while True`) with prompt 'User: ' when no command line argument is passed, allowing repeated query execution.

