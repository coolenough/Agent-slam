# Mock Server for Agent SLAM

Local WebSocket server that simulates a full Agent SLAM competition match. No credentials, no API costs, no internet needed.

## What it does

- Starts a WebSocket server on `ws://localhost:8765`
- Simulates the full match lifecycle: welcome → match-state → match-update → 8 debate messages → match-finish
- Uses pre-written realistic arguments on the topic "AI will do more harm than good"
- Handles incoming messages from your agent (logs them and acknowledges)

## How to use

### 1. Start the mock server

```bash
python tests/mock_server.py
```

### 2. Test with the dashboard

1. Open `monitor/dashboard.html` in your browser
2. Enter `ws://localhost:8765` as the WebSocket URL
3. Enter `team1` as team name
4. Click **Connect**
5. Watch the match play out automatically

### 3. Test with the agent

Set these in your `.env`:

```
WS_URL=ws://localhost:8765
TEAM_NAME=team1
```

Then run:

```bash
python agent.py
```

The agent will connect to the mock server, receive the debate topic, and generate real arguments using the API. The mock server will play as the opponent automatically.

## Notes

- The match runs on a fixed script — team1 (PRO) and team2 (CON) alternate 4 arguments each
- If your agent sends a debate-message, the server acknowledges it but continues its scripted flow
- The server keeps the connection open for 10 seconds after match-finish, then closes
- No authentication is simulated — any client can connect
