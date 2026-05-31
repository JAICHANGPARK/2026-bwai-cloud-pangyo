---
description: Generate Gemma 4 Structured Output Code
---

1. Read the rules in [gemma4_so.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_so.md).
2. Write or update the Python script at `hands-on/structured_output.py` using `httpx` and `asyncio` to fetch JSON structured outputs.
3. Constrain the model with a JSON schema containing `name`, `role`, `skills`, and `experience_years`.
4. Configure JSON mode parameters: `"format": "json"` for Ollama, `"response_format": {"type": "json_object"}` for LM Studio/llama.cpp.
5. Parse and validate the accumulated output using `json.loads` before printing validation status.
