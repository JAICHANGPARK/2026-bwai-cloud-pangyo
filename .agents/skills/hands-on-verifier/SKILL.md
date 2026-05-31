---
name: hands-on-verifier
description: Verify that generated hands-on code scripts run successfully and interface with local LLMs as expected.
---

# Hands-On Verifier Skill

This skill allows the agent to automatically verify the correctness and execution of the generated hands-on scripts (`hands-on/main.py`, `hands-on/function_calling.py`, `hands-on/structured_output.py`, `hands-on/thinking_toggle.py`).

## When to use this skill
- Use this after generating or editing any code in the `hands-on/` directory to ensure that it has no syntax errors and runs successfully.
- Use this to verify that the generated code satisfies all the specific requirements from the rules files.

## Verification Checklist

### 1. Code Quality & Syntax Check
- Verify that the target python file exists and is located in the `hands-on/` directory.
- Perform a syntax check (e.g., by running `python -m py_compile <file>`).

### 2. Functional & Integration Execution
- Read the `.env` configuration file in the `hands-on/` folder to check which provider (`LLM_PROVIDER`) is selected.
- If the corresponding local LLM server is online, execute a dry run of the script with a test prompt.
- Capture the output and verify:
  - Streaming works as expected.
  - The model's reasoning/thinking process (e.g., inside `<think>` tags) is successfully parsed and styled (or filtered out if in `--no-think` mode for `thinking_toggle.py`).
  - Output is printed cleanly without tracebacks.

### 3. Verification Report
- Summarize the verification status of the code (e.g., syntax correctness, expected file locations, configuration matching).
- Report any issues found in the script logic or environment variables.
