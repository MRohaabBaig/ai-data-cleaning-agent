# Plan: Make AI Agent Interactive

The goal is to transform the hard-coded execution of the LangGraph workflow in agent.py into an interactive CLI experience.

## Requirements
1. Interaction Flow: Welcome message, choice between Direct Text and CSV, capture inputs, and custom prompt.
2. Robustness: Handle missing files, empty inputs, and clean CSV conversion.
3. Integration: Pass values into app.invoke() while maintaining LangGraph structure.

## Implementation Steps
1. Add 'import os' to agent.py.
2. Replace the hard-coded main block with an interactive loop for input collection.
3. Implement CSV reading with pandas and error handling for missing files.
4. Collect user_prompt and invoke the graph.

## Verification Strategy
- Test direct text input.
- Test valid CSV input.
- Test invalid CSV path.
- Test empty input fields.
