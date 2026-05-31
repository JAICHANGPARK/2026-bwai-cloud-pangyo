# Generate Gemma 4 Structured Output Code

Write or update the Python script at `hands-on/structured_output.py` to implement Structured Output generation with local LLM providers (Ollama, LM Studio, llama.cpp).

## Guidelines & Requirements:
1. **Workspace Rules:** Strictly follow the rules defined in [gemma4_so.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_so.md).
2. **Library & Async:** Use `httpx` and write the code using `asyncio` with streaming (`stream=True`).
3. **JSON Schema Constraint:** Instruct the model via system prompts to follow a JSON schema with fields: `name`, `role`, `skills`, and `experience_years`.
4. **Provider-Specific JSON Mode Configuration:**
   - **Ollama:** Set `"format": "json"` in the API request payload.
   - **LM Studio / llama.cpp:** Set `"response_format": {"type": "json_object"}` in the API request payload.
5. **Validation:** Accumulate streamed tokens and validate the final text using `json.loads`. Print the validation status on the screen.
6. **Error & Keyboard Interrupt Handling:** Provide detailed connection error handling and handle `KeyboardInterrupt` to exit gracefully.
7. **Target File:** Save the generated code strictly to `hands-on/structured_output.py`.
