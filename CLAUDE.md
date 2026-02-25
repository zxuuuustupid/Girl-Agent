# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GirlAgent is an AI girlfriend chatbot built with Python that uses LLM (DeepSeek/OpenAI-compatible APIs) to generate conversational responses. The agent features a reactive action system that can perform various interactions (asking for gifts, giving gifts, intimate actions, etc.) based on conversation context.

## Running the Application

**CLI version:**
```bash
python src/main.py
```

**GUI version (PyQt6):**
```bash
python src/main_gui.py
```

## Architecture

### Core Components

The agent follows a **Plan-Act-Respond** loop pattern:

1. **Agent** (`src/agent/base.py`) - Central coordinator that orchestrates the conversation flow
   - Maintains a `Memory` of recent conversation history
   - Uses a `Planner` to generate chain-of-thought reasoning
   - Delegates actions to `ActionExecutor`
   - Iteratively processes actions until a terminal action is reached

2. **Memory System** (`src/agent/memory.py`)
   - Short-term memory with configurable size (default: 20 items)
   - Stores conversation turns with roles: `user`, `assistant`, `action_result`
   - When memory exceeds size limit, old memories are asynchronously moved to long-term storage (RAG placeholder)

3. **Planner** (`src/agent/plan.py`)
   - Generates a reasoning plan using chain-of-thought prompting
   - Plans serve as context for response generation, not rigid execution scripts

4. **Action System** (`src/agent/action.py`, `src/tools/`)
   - **Tool Interface** (`tools/tool_interface.py`): Abstract base class with `name()`, `description()`, `run()`, `format_result()`
   - **ToolRegistry** (`tools/registry.py`): Registers and retrieves tool instances
   - **Built-in Tools** (`tools/chat_tools.py`): `chat`, `ask_gift`, `give_gift`, `ask_coins`, `intimate_action`, `angry_end`
   - Tools can have side effects (user input via console) and return formatted results

5. **LLM Service** (`src/llm/base.py`)
   - Abstract `LLMService` class with `DeepSeekService` implementation
   - Uses OpenAI-compatible API (can work with any OpenAI-compatible endpoint)
   - All calls are synchronous, async wrapper happens at agent level

### Prompt Building (`src/prompts/`)

- **Identity** (`identity.py`): Constructs base persona from config + personality module
- **Builder** (`builder.py`): Builds prompts for planning and response generation
  - `build_plan_prompt()`: Formats chain-of-thought prompt with history
  - `build_response_prompt()`: Formats response prompt with plan, history, and executed actions
- **Response Template** (`response.py`): Main prompt template that includes:
  - Identity/personality
  - Available tools with descriptions
  - Conversation history
  - Current user message
  - Plan reference
  - Previously executed actions
  - Requires JSON output with `response` (string) and `action` (name + params)

### Personality System

Personalities are loaded dynamically from `src/prompts/personalities/*.py`:
- Each personality module exports a `PERSONALITY` string constant
- Configured via `AGENT_SETTINGS["personality"]` in `src/config/settings.py`
- Built-in personalities: `slapper`, `slaver`, `cute`, `mature`

### Configuration (`src/config/settings.py`)

- `DEEPSEEK_SETTINGS`: API key, base URL, model name
- `AGENT_SETTINGS`: Name, age, gender, occupation, personality
- `MEMORY_SIZE`: Short-term memory capacity

## Key Data Flow

```
User Input → Agent.process_input()
    ↓
Memory.add_memory(user_input)
    ↓
Planner.create_plan() → LLM call → plan
    ↓
Agent._gen_response(plan) → LLM call → JSON response
    ↓
Parse response: {thought, action_data}
    ↓
[Loop] ActionExecutor.execute(action_name) → Tool.run() → result
    ↓
Memory.add_memory(action_result)
    ↓
_gen_response(plan, actions) → LLM call → JSON response
    ↓
[Continue until action in {"chat", "end", "angry_end"}]
```

## Development Notes

- **GUI version runs async agent calls in QThread** to prevent UI blocking (`main_gui.py:30-48`)
- **Agent responses are always JSON** containing `response` field and optional `action` with `name`/`params`
- **Tools must be registered** in `ToolRegistry._register_default_tools()` to be available
- **Memory overflow triggers async RAG save** (currently a stub with `asyncio.sleep`)
- **Plan text is stripped of `# ` headers** when passed to response prompt (`builder.py:33-38`)
- When adding new tools, implement all 4 required methods and add to `ToolRegistry` initialization
