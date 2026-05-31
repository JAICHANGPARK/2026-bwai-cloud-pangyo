# Generate Gemma 4 Function Calling Code

Write or update the Python script at `hands-on/function_calling.py` to implement Function Calling with local LLM providers (Ollama, LM Studio, llama.cpp).

## Guidelines & Requirements:
1. **Workspace Rules:** Strictly follow the rules defined in [gemma4_fc.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_fc.md).
2. **Library & Async:** Use `httpx` and write the code using `asyncio`.
3. **Flow Structure:**
   - **Step 1 (Tool Assessment):** Send the request to LLM with `tools` metadata (non-streaming: `stream=False`). Define a tool `get_current_weather(location)` that fetches real weather data from the `wttr.in` JSON API (`https://wttr.in/{location}?format=j1`).
   - **Step 2 (Tool Execution & Output):** Run the tool if requested by the model, append tool execution results, and stream the final answer (`stream=True`).
4. **Environment:** Dynamically load `LLM_PROVIDER`, `LLM_API_URL`, and `LLM_MODEL` using `python-dotenv`.
5. **Provider Discrepancy:** Handle both Ollama's native tool calling response format and OpenAI-compatible format (LM Studio, llama.cpp) correctly.
6. **Error & Keyboard Interrupt Handling:** Provide detailed connection error handling and handle `KeyboardInterrupt` to exit gracefully.
7. **Target File:** Save the generated code strictly to `hands-on/function_calling.py`.
