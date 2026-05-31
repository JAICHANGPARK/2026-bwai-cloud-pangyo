# Generate Gemma 4 Basic Streaming Code

Write or update the Python script at `hands-on/main.py` to implement basic streaming chat with local LLM providers (Ollama, LM Studio, llama.cpp).

## Guidelines & Requirements:
1. **Workspace Rules:** Strictly follow the rules defined in [gemma4_hands_on.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_hands_on.md).
2. **Library:** Use `httpx` as the HTTP client.
3. **Environment:** Use `python-dotenv` to load `.env` configuration. Retrieve `LLM_PROVIDER`, `LLM_API_URL`, and `LLM_MODEL` dynamically.
4. **Thinking Parsing:** Catch `<think>` and `</think>` tags and print the model's thinking process in gray/dim text.
5. **Interactive Loop:** Implement a terminal loop that waits for user input ("User: "), streams the response, and exits cleanly when the user inputs 'exit' or 'quit'.
6. **Error Handling:** Catch connection errors gracefully and handle `KeyboardInterrupt` to exit without traceback.
7. **Target File:** Save the generated code strictly to `hands-on/main.py`.
