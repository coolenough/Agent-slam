# Testing Approach — Agent SLAM 2026

## Method: Perplexity-as-Opponent

We test the debate bot by using Perplexity AI (or ChatGPT) to generate opponent arguments manually. This gives realistic, high-quality opposition without requiring a second bot or the competition sandbox.

### How It Works

1. Start the bot against a local WebSocket test server
2. The bot sends its opening argument automatically
3. Copy the bot's argument into Perplexity with a prompt like:
   > "You are debating the CON side of: [topic]. Respond to this argument: [paste bot's message]"
4. Paste Perplexity's response back as the opponent's message
5. The bot generates its next argument
6. Repeat until the match ends or you've seen enough turns

### What to Evaluate

After each test run, check the bot's output against these criteria:

| Check | Target | Red Flag |
|---|---|---|
| Response time | < 30 seconds | > 90 seconds (timeout risk) |
| Character count | 1800–2800 chars | < 1500 (too short) or trimming fires (too long) |
| Source URLs | Different each turn | Same URL cited twice |
| Opponent quoting | Direct quotes in every rebuttal | Generic "the opponent is wrong" |
| Escalation | New argument each turn | Same 3 points repeated |
| Tone | Assertive, offensive | "While it's true..." or "You're right that..." |
| Closing | Starts with "In conclusion," | Bland mid-debate rebuttal as final message |
| Phase transitions | Opening → Rebuttal → Cross-Exam → Defense → Closing | Premature closing |

### Log Files

Every run creates a log file in `logs/agent_YYYYMMDD_HHMMSS.log`. Check these for:
- `IT IS OUR TURN` → `Sent argument` timestamps (measure latency)
- `call_mode=` entries (should be "normal" or "fast" for most turns)
- `web_search_requests` count
- Any `ERROR` lines

### Future Plan

Build a dedicated testing dashboard that:
- Connects to the local test server
- Has a text input for pasting Perplexity responses
- Shows bot output, character counts, timing, and phase transitions
- Allows setting match time for testing closing detection
- Keeps a scorecard for manual evaluation

This will replace the current manual copy-paste workflow with a streamlined UI.
