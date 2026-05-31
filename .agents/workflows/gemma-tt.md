---
name: gemma-tt
description: Generate Gemma 4 Thinking Toggle Code
---

1. Read the rules in [gemma4_tt.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_tt.md).
2. Write or update the Python script at `hands-on/thinking_toggle.py` using `httpx` and `asyncio`.
3. Parse CLI flags: if `--no-think` is passed, disable thinking display.
4. For Ollama: if `--no-think` is set, add `"think": false` and `options: {"think": false}` in the API payload.
5. For all providers: filter out all text tokens between `<think>` and `</think>` on the client-side if thinking is disabled.
