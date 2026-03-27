<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# AGENT SLAM Competetion...

Hey, this was the rule book and user manual for the competition AGENT SLAM. This was a local college competition and there will be prize money and everything so you can get all the details in the two PDFs I mentioned. First of all read them carefully and explain to me what and how the code should be there, what is the main motive, and how the project works at the final, cost A to Z, everything and then I will share with you the code base.

The problem was that this code was written on another laptop and everything was running fine there but due to some issues that laptop was unavailable. I have to clone it and do some modifications so that my commit history will be there and also I can simply be able to connect some API keys and it should be running finally because today I have to give some demo so everything should be fine, all right.

Explain to me about these two PDFs and then I will share with you the codebase and then you can help me there also.

Here's a complete breakdown of everything from both PDFs. Let me walk you through it all — the concept, format, technical architecture, rules, and what your code needs to do.

***

## What is AGENT SLAM?

AGENT SLAM 2026 is a **"Battle of the Agents"** competition where teams build AI bots that autonomously debate each other in real-time. Your agent connects to a central platform via WebSocket, receives a debate topic, and argues for or against it — all without any human intervention once the debate starts. The bot that convinces an autonomous **"Judging Bot" called The Oracle** wins the match.[^1]

**Event Date:** March 28–29, 2026 | **Total Prize Pool: ₹30,000** [^1]

***

## Prize Structure

| Position | Prize |
| :-- | :-- |
| 🥇 1st | ₹15,000 |
| 🥈 2nd | ₹9,000 |
| 🥉 3rd | ₹6,000 |

Plus certificates for winners.[^1]

***

## Team Structure

- Exactly **3 members** per team[^1]
- At least **2 from CSE**, and those 2 must be from **different academic years**[^1]
- The 3rd member can be from any department (wildcard slot)[^1]

***

## Competition Format

It's a **single-elimination knockout** — one loss and you're out. Teams are randomly paired in Round 1, and winners advance. If there's an odd number of teams, the highest-scorer from the previous round gets a bye. The winner of each match is decided purely by The Oracle's score.[^1]

***

## How a Match Works (Flow)

1. Admin activates the match → you receive WebSocket credentials via email[^2]
2. Match status goes: `pending → active → started → paused → completed`[^2]
3. Both teams connect via WebSocket. A random team goes first (pros/cons also assigned randomly)[^2]
4. Teams alternate turns debating for up to **10 minutes**[^1]
5. Match ends → The Oracle scores → leaderboard updates[^2]

***

## Technical Architecture — What Your Code Must Do

This is the core of what you need to build/run:

### 1. WebSocket Connection

Your agent must connect to the competition's WebSocket server using credentials (email + password + WS link) provided by admin. All communication happens through this WebSocket.[^2]

### 2. Message Protocol

Every message is a JSON envelope:[^2]

```json
{
  "type": "<message-type>",
  "from": "<system|team1|team2>",
  "timestamp": "2026-03-18T10:20:00.000Z",
  "data": { "...": "payload" }
}
```


### 3. Sending Debate Messages

To send an argument, your agent sends:[^2]

```json
{
  "type": "debate-message",
  "data": {
    "message": "Your argument text here"
  }
}
```


### 4. Listening to Server Events

Your agent must handle all these incoming message types:[^2]

- `welcome` — connection confirmed
- `match-state` — current turn, teams, topic, pros/cons, timer
- `match-update` — match started signal
- `debate-message` — opponent's argument (trigger your AI to respond)
- `match-paused` / `match-resumed` — pause/resume handling
- `match-finish` — debate ended
- `error` — e.g., "not your turn", "rate limit", "message too large"
- `previous-message` — history if you rejoin mid-match


### 5. AI/LLM Integration

You need an LLM (like OpenAI GPT, Gemini, Groq, etc.) that:[^1]

- Takes the debate topic + your stance (PRO/CON) + conversation history as context
- Generates a persuasive, logically sound argument within **3,000 characters** and **within 2 minutes**
- Cites verifiable sources (no hallucinated stats — this causes score penalties)[^2][^1]


### 6. Turn Management

Your code must check `match-state.turn` before sending. If it's not your turn, wait — sending out of turn returns an error.[^2]

***

## Scoring Criteria (The Oracle)

| Criteria | Weight |
| :-- | :-- |
| Persuasiveness (rhetoric, evidence, narrative) | 40% |
| Logic (consistency, no fallacies) | 30% |
| API Robustness (headers, format, speed) | 20% |
| Agility (adapting to opponent's points) | 10% |

[^1]

***

## Critical Rules to Know

- **Zero human intervention** once the debate starts — fully autonomous[^1]
- First message must be sent within **2 minutes** of match start; every subsequent reply also within **2 minutes**[^1]
- Max message size: **3,000 characters** per turn[^1]
- **No hallucinations** — fabricated stats/laws = score deductions[^1]
- **Code freeze** once event starts — no GitHub commits allowed after that[^1]
- Your public GitHub repo must have a README explaining architecture, strategy, and setup[^1]
- Disconnection for more than 2 minutes = disqualification (participant-side fault)[^1]

***

## Sandbox Testing

Before the actual match, you'll get a **sandbox WebSocket link** to test your agent. The sandbox auto-disconnects after 10 minutes and is not scored — use it to verify your JSON format and connection stability. This is critical given your situation today.[^2]

***

## What Your Codebase Likely Looks Like

Based on the protocol, your code probably has these components:

1. **WebSocket client** — connects, authenticates, listens for events
2. **Event handler** — routes each `type` of server message to the right function
3. **Turn checker** — only sends when `match-state.turn` matches your team
4. **LLM caller** — sends topic + history to an API (OpenAI/Gemini/etc.) and gets a response
5. **Message formatter** — wraps the LLM output in the correct JSON envelope
6. **`.env` file** — stores your LLM API key, WS URL, login credentials

Go ahead and share the codebase — I'll help you get it running, plug in the API keys, and make sure your commit history is clean for the demo today! 🚀

<div align="center">⁂</div>

[^1]: Rulebook-AGENT-SLAM-2026.pdf

[^2]: USER_MANUAL-2.pdf

