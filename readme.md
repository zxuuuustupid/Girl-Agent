<div align="center">

# 💕 Girl Agent

**An extensible AI companion chatbot powered by LLM, featuring a reactive action system and customizable personalities.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-Compatible-7C3AED?style=for-the-badge)](https://deepseek.com)
[![OpenAI API](https://img.shields.io/badge/OpenAI_API-Compatible-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com)
[![PySide6](https://img.shields.io/badge/PySide6-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)

<br>

<table>
  <tr>
    <td align="center">
      <img src="assets/kato.JPG" alt="Kato Megumi" width="220" style="border-radius: 12px"><br>
      <sub><b>Kato Megumi</b></sub>
    </td>
    <td align="center">
      <img src="assets/miku.png" alt="Nakano Miku" width="220" style="border-radius: 12px"><br>
      <sub><b>Nakano Miku</b></sub>
    </td>
    <td align="center">
      <img src="assets/marin.JPG" alt="Kitagawa Marin" width="220" style="border-radius: 12px"><br>
      <sub><b>Kitagawa Marin</b></sub>
    </td>
  </tr>
</table>

<br>

> _Though named "Girl Agent", this framework is fully generic — create any AI companion you want._
> _The name simply reflects the author's personal interests. 😄_

</div>

---

## ✨ Highlights

| Feature                        | Description                                                                                                                                |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 🧠 **Plan‑Act‑Respond Loop**   | Chain-of-thought reasoning drives every reply — the agent _thinks_ before it speaks                                                        |
| 🎭 **Swappable Personalities** | Hot-swap between `cute`, `tsundere`, `idol`, `gamer`, `neighbor` and more — or write your own                                              |
| 🔧 **Reactive Action System**  | Built-in tools (`chat`, `ask_gift`, `give_gift`, `ask_coins`, `intimate_action`, `angry_end`) orchestrate dynamic, multi-turn interactions |
| 🖥️ **Dual Interface**          | CLI for quick testing, modern **PySide6/QML** GUI for daily use                                                                            |
| 🔌 **Multi-Provider LLM**      | Seamlessly switch between **DeepSeek · Zhipu GLM · MiniMax · OpenRouter** — any OpenAI-compatible endpoint works                           |
| 💾 **Memory System**           | Short-term conversation memory with async long-term RAG storage (extensible)                                                               |
| 📦 **Standalone Build**        | Ship as a single executable via PyInstaller                                                                                                |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- An API key from a supported LLM provider (DeepSeek, Zhipu, MiniMax, OpenRouter, etc.)

### 1 · Clone & Install

```bash
git clone https://github.com/zxuuuustupid/Girl-Agent.git
cd Girl-Agent
pip install -r requirements.txt
```

### 2 · Configure

Create a `.env` file in the project root (recommended), or edit `src/config/settings.py` directly:

```dotenv
# .env — pick your provider and fill in the key
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_BASE=https://api.deepseek.com      # optional, defaults shown
DEEPSEEK_MODEL=deepseek-chat                     # optional

# — or use another provider —
# ZHIPU_API_KEY=...
# MINIMAX_API_KEY=...
# OPENROUTER_API_KEY=...
```

Customize the agent's persona in `src/config/settings.py`:

```python
AGENT_SETTINGS = {
    "name": "Megumi",       # Display name
    "age": 19,              # Character age
    "gender": "女",         # Gender
    "occupation": "学生",   # Occupation
    "personality": "cute"   # Module name from src/prompts/personalities/
}
```

### 3 · Run

**CLI mode** — quick & simple:

```bash
python src/main.py
```

**GUI mode** — full desktop experience:

```bash
python src/main_gui.py
```

---

## 🎭 Personality System

Personalities live in `src/prompts/personalities/` as plain Python files exporting a `PERSONALITY` string constant. The agent loads the named module at startup.

| Built-in      | Vibe                                 |
| ------------- | ------------------------------------ |
| `cute`        | Sweet, affectionate, upbeat          |
| `tsundere`    | Hot-cold, secretly caring            |
| `idol`        | Energetic, sparkly, fan-service      |
| `gamer`       | Competitive, meme-savvy              |
| `neighbor`    | Warm, grounded, girl-next-door       |
| `shynakamura` | Shy, soft-spoken, gradually opens up |

### Creating a Custom Personality

```python
# src/prompts/personalities/my_char.py

PERSONALITY = """
You are Aria, a mysterious librarian who speaks in riddles
and quotes classical literature. You are warm but enigmatic,
always hinting at deeper truths hidden between the lines...
"""
```

Then set `"personality": "my_char"` in `AGENT_SETTINGS` — done.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Input                         │
└──────────────────────────┬──────────────────────────────┘
                           ▼
                 ┌───────────────────┐
                 │   Agent (core)    │
                 │  ┌─────────────┐  │
                 │  │   Memory    │  │  ◄── Short-term (20 turns)
                 │  │   System    │  │      + async RAG overflow
                 │  └─────────────┘  │
                 │  ┌─────────────┐  │
                 │  │   Planner   │  │  ◄── Chain-of-thought via LLM
                 │  └─────────────┘  │
                 │  ┌─────────────┐  │
                 │  │  Executor   │──┼──► ToolRegistry ──► Tools
                 │  └─────────────┘  │        │
                 └────────┬──────────┘        ▼
                          │            ┌──────────────┐
                          │            │  chat_tools  │
                          │            │  ask_gift    │
                          │            │  give_gift   │
                          │            │  ask_coins   │
                          │            │  intimate    │
                          │            │  angry_end   │
                          │            └──────────────┘
                          ▼
              ┌───────────────────────┐
              │  LLM Service Layer    │
              │  (OpenAI-compatible)  │
              ├───────────────────────┤
              │ DeepSeek │ Zhipu GLM  │
              │ MiniMax  │ OpenRouter  │
              └───────────────────────┘
```

### Data Flow

```
User Input  →  Memory.add(user)
            →  Planner.create_plan()  →  LLM ──► plan
            →  Agent._gen_response(plan)  →  LLM ──► JSON { response, action }
            →  [Loop] ActionExecutor.execute(action)
                     ↳ Tool.run()  →  result
                     ↳ Memory.add(action_result)
                     ↳ _gen_response(plan, actions)  →  LLM ──► JSON
            →  Terminal action reached (chat | end | angry_end)
            →  Return outputs
```

---

## 📂 Project Structure

```
Girl-Agent/
├── assets/                  # Icons & character images
├── src/
│   ├── agent/
│   │   ├── base.py          # Core agent loop (Plan-Act-Respond)
│   │   ├── memory.py        # Short-term + async RAG memory
│   │   ├── plan.py          # CoT planner
│   │   └── action.py        # Action model & executor
│   ├── config/
│   │   ├── settings.py      # All configurable settings & env vars
│   │   └── provider.py      # LLM provider selector
│   ├── gui/
│   │   ├── app_bridge.py    # PySide6 ↔ QML bridge
│   │   └── qml/             # QML UI files
│   ├── llm/
│   │   └── base.py          # LLM service abstraction & implementations
│   ├── prompts/
│   │   ├── builder.py       # Prompt construction for plan & response
│   │   ├── identity.py      # Persona identity builder
│   │   ├── response.py      # Response prompt template
│   │   └── personalities/   # Pluggable personality modules
│   │       ├── cute.py
│   │       ├── tsundere.py
│   │       ├── idol.py
│   │       ├── gamer.py
│   │       ├── neighbor.py
│   │       └── ...
│   ├── tools/
│   │   ├── tool_interface.py # Abstract Tool base class
│   │   ├── registry.py       # Tool registration & lookup
│   │   └── chat_tools.py     # Built-in tool implementations
│   ├── rag/                   # RAG long-term memory (extensible)
│   ├── main.py                # CLI entry point
│   └── main_gui.py           # GUI entry point
├── tests/
├── requirements.txt
├── main.spec                  # PyInstaller build spec
└── LICENSE
```

---

## 🔧 Tool System

Tools are the agent's _hands_. Each tool implements four methods:

| Method            | Purpose                                                           |
| ----------------- | ----------------------------------------------------------------- |
| `name()`          | Unique identifier used in action dispatch                         |
| `description()`   | Shown to the LLM so it knows when/how to invoke the tool          |
| `run()`           | Executes the tool logic, may have side-effects (e.g. GUI prompts) |
| `format_result()` | Converts the raw result into a human-readable string for memory   |

### Built-in Tools

| Tool              | Action                                                       |
| ----------------- | ------------------------------------------------------------ |
| `chat`            | Standard conversational reply                                |
| `ask_gift`        | Ask the user for a specific gift (with accept/refuse dialog) |
| `give_gift`       | Give the user a gift                                         |
| `ask_coins`       | Request virtual coins (with numeric input dialog)            |
| `intimate_action` | Narrate an intimate/roleplay action                          |
| `angry_end`       | End the conversation angrily                                 |

### Adding a New Tool

1. Create a class extending `Tool` in `src/tools/`
2. Implement `name()`, `description()`, `run()`, `format_result()`
3. Register it in `ToolRegistry._register_default_tools()` inside `src/tools/registry.py`

---

## 📦 Packaging as Standalone App

Build a distributable executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --clean --noconfirm main.spec
```

The output binary will be in `dist/`.

---

## 🛣️ Roadmap

- [x] CLI chat interface
- [x] PySide6/QML desktop GUI (v1.1)
- [x] Multi-provider LLM support (DeepSeek, Zhipu, MiniMax, OpenRouter)
- [x] PyInstaller standalone packaging
- [ ] RAG-based long-term memory implementation
- [ ] Streaming response support
- [ ] Voice input/output integration
- [ ] Plugin marketplace for community personalities & tools

---

## 🤝 Contributing

Contributions are welcome! Whether it's a new personality, a tool plugin, a bug fix, or a feature idea — feel free to open an issue or submit a PR.

1. Fork the repository
2. Create your feature branch: `git checkout -b feat/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright © 2025 Zhixu Duan

---

<div align="center">

**If you find this project interesting, consider giving it a ⭐!**

Made with ❤️ and a love for anime

</div>
