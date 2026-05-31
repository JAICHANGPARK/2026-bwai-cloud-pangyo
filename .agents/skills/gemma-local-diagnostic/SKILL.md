---
name: gemma-local-diagnostic
description: Diagnose if local LLM API servers (Ollama, LM Studio, llama.cpp) and python environments are running and configured properly.
---

# Gemma Local Diagnostic Skill

This skill diagnoses the user's local development environment to ensure that local LLM API servers are running and accessible, and that python dependencies are correctly installed.

## When to use this skill
- Use this when the user reports connection errors, API timeouts, or model loading issues.
- Use this to verify the initial environment setup of the hands-on participant before running the scripts.

## Diagnostics Checklist

### 1. Local LLM Server Diagnostics
The agent should perform HTTP tests to check the status of local servers:
- **Ollama**: Query `GET http://localhost:11434/api/tags` to check if running and find downloaded models (e.g., `gemma4:e4b`).
- **LM Studio**: Query `GET http://localhost:1234/v1/models` to verify the local server is running.
- **llama.cpp**: Query `GET http://localhost:8080/health` or `GET http://localhost:8080/v1/models` to verify the local server is running.

### 2. Python Environment & Dependency Check
- Inspect the root and `hands-on/` directories for virtual environments (e.g., `.venv`).
- Check if critical packages are installed:
  - `httpx`
  - `python-dotenv`
- If packages are missing, suggest the installation command (e.g., using `uv pip install httpx python-dotenv` or `pip install httpx python-dotenv`).

### 3. Reporting Results
Provide a structured report in the chat:
- **LLM Server Status**: Which server is online, and which models are loaded.
- **Python Dependencies**: Current status of packages.
- **Actionable Steps**: What the user needs to do next if anything is offline or missing.
