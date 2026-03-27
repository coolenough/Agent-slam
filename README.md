# Agent SLAM 2026 — AI Debate Agent

An autonomous AI debate agent built for **Agent SLAM 2026**, a live competitive debate tournament where student-built AI agents argue complex topics in Finance, Marketing, and Ethics. The agent connects to a central WebSocket server, receives a debate topic and stance (PRO/CON), and argues fully autonomously — zero human intervention once the match starts.

---

## Architecture

```
agent.py               ← Entry point. Run this on match day.
src/
  config.py            ← Loads .env, exposes all constants
  state_machine.py     ← Tracks live match state (turn, stance, phase, history)
  ws_client.py         ← WebSocket connection, auto-reconnect, message routing
  debate_engine.py     ← Calls Claude API with web_search tool, returns argument
  strategy.py          ← Builds system + user prompt based on current debate phase
tests/
  mock_server.py       ← Local mock competition server for offline testing
monitor/
  dashboard.html       ← Real-time match spectator UI (read-only)
logs/                  ← Per-session log files auto-created at runtime
```

### Data Flow Per Turn

1. `ws_client` receives `match-state` or `debate-message` → updates `state_machine`
2. `state_machine` detects it is our turn → triggers `debate_engine`
3. `strategy.py` builds a phase-aware prompt (opening / rebuttal / cross-examination / defense / closing)
4. `debate_engine` calls Claude API (`claude-sonnet-4-5` + `web_search` tool)
5. Response trimmed to under 2800 characters → sent as `debate-message` JSON over WebSocket
6. `state_machine` records our message, increments counter, waits for next turn

---

## Debate Strategy

The agent uses a **5-phase debate system** with automatic phase detection:

| Phase | Trigger | Goal |
|---|---|---|
| `opening` | `message_count == 0` | State position, 3 sourced arguments |
| `rebuttal_first` | `message_count == 1` | Attack opponent's weakest claim specifically |
| `cross_examination` | `message_count 2–3` | Expose logical gaps, apply pressure |
| `defense` | `message_count 4+` | Hold ground, deepen evidence |
| `closing` | `seconds_remaining < 180` | Synthesize wins, memorable final statement |

Key advantages:
- **Phase-aware prompting** — most teams use a flat "debate" prompt
- **Closing detection** — auto-switches strategy in final 3 minutes
- **Real source citation** — `web_search` tool fetches actual URLs; no hallucinated stats
- **Agility** — system prompt explicitly instructs the agent to quote opponent's exact words and dismantle them
- **Anti-hallucination** — if uncertain about a fact, the agent argues from logic, not fabricated data

---

## Frameworks, APIs & Models Used

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| AI Model | Anthropic Claude (`claude-sonnet-4-5`) |
| Web Search | Anthropic `web_search_20250305` tool |
| WebSocket | `websockets` library (async) |
| Config | `python-dotenv` |

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/shajith240/Agent-slam.git
cd Agent-slam
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
WS_URL=<match WebSocket URL from admin>
SANDBOX_WS_URL=<sandbox WebSocket URL from admin>
TEAM_EMAIL=<your login email>
TEAM_PASSWORD=<your login password>
TEAM_NAME=<team1 or team2 as assigned>
```

---

## Running the Agent

### Live match
```bash
python agent.py
```

### Sandbox / testing mode
```bash
python agent.py --sandbox
```

### Local mock server (for offline testing)
```bash
# Terminal 1 — start mock server
python tests/mock_server.py

# Terminal 2 — connect agent to mock server
python agent.py
```

---

## Competition Rules Compliance

- ✅ First message sent within 2 minutes of match start
- ✅ Each reply sent within 2 minutes (85s internal hard cutoff guard)
- ✅ Max 3000 characters per message (hard-capped at 2800 for safety)
- ✅ Zero human intervention once match starts
- ✅ All factual claims cited with real source URLs via web search
- ✅ Auto-reconnect within the 2-minute disconnection window
- ✅ No offensive or toxic content in arguments
