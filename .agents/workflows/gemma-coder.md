---
name: gemma-coder
description: Generate Gemma 4 Basic Streaming Code
---

1. Read the rules in [gemma4_hands_on.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_hands_on.md).
2. Write or update the Python script at `hands-on/main.py` using `httpx` and `asyncio` to implement a terminal interactive chat loop.
3. Ensure it catches `<think>` and `</think>` tags to print the thinking process in dim/gray text.
4. Add connection error and keyboard interrupt handling.
