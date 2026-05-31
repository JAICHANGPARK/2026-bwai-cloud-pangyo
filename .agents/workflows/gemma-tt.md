# Generate Gemma 4 Thinking Toggle Code

Write or update the Python script at `hands-on/thinking_toggle.py` to implement a CLI flag-based thinking toggle with local LLM providers (Ollama, LM Studio, llama.cpp).

## Guidelines & Requirements:
1. **Workspace Rules:** Strictly follow the rules defined in [gemma4_tt.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_tt.md).
2. **Library & Async:** Use `httpx` and write the code using `asyncio` with streaming (`stream=True`).
3. **CLI Argument Parsing:** Parse command-line arguments to toggle thinking. If `--no-think` is passed, disable thinking process display.
4. **API and Client-side Control:**
   - **Ollama:** If thinking is disabled, send `"think": false` in the API payload and set `options: {"think": false}`.
   - **Client-side Filtering (All Providers):** Keep track of `<think>` and `</think>` tags.
     - If thinking is enabled: Print `[생각 과정 시작...]` and output thinking process tokens in gray.
     - If thinking is disabled: Filter and skip printing all tokens between `<think>` and `</think>`.
5. **Error & Keyboard Interrupt Handling:** Provide detailed connection error handling and handle `KeyboardInterrupt` to exit gracefully.
6. **Target File:** Save the generated code strictly to `hands-on/thinking_toggle.py`.
