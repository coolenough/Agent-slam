"""
Local mock WebSocket server that simulates the Agent SLAM competition server.
Run: python tests/mock_server.py
Starts on ws://localhost:8765 — no credentials needed.
"""

import asyncio
import json
import logging
import time
import random
from datetime import datetime, timezone

import websockets

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [MOCK] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("mock_server")

PORT = 8765

# ---------------------------------------------------------------------------
# Pre-written argument pools
# ---------------------------------------------------------------------------

TEAM1_ARGS = [
    (
        "AI-driven automation threatens to displace 85 million jobs globally by 2025 "
        "according to the World Economic Forum. This is not speculative — we are already "
        "seeing mass layoffs in manufacturing, customer service, and data entry roles. The "
        "economic disruption this causes disproportionately affects low-income workers who "
        "lack resources to reskill. "
        "(Source: https://www.weforum.org/reports/the-future-of-jobs-report-2020)"
    ),
    (
        "My opponent has failed to address the surveillance crisis that AI enables. Facial "
        "recognition systems deployed by authoritarian governments have led to the "
        "imprisonment of over one million Uyghurs in China. When a technology becomes the "
        "primary tool of oppression at this scale, its harm is undeniable. "
        "(Source: https://www.bbc.com/news/world-asia-china-22278037)"
    ),
    (
        "The misinformation epidemic powered by AI-generated deepfakes threatens democratic "
        "processes worldwide. A 2023 MIT study found AI-generated fake news spreads six "
        "times faster than real news on social media. When citizens cannot distinguish truth "
        "from fabrication, democracy itself collapses. "
        "(Source: https://news.mit.edu/2018/study-twitter-false-news-travels-faster-true-stories-0308)"
    ),
    (
        "In conclusion — I have demonstrated three irreversible harms of AI: mass "
        "unemployment affecting 85 million workers, state-sponsored surveillance and "
        "oppression, and a deepfake misinformation crisis destroying democratic trust. My "
        "opponent offered theoretical future benefits while I cited documented present "
        "harms. The burden of proof is on those claiming AI helps humanity — and that "
        "burden has not been met. The motion stands."
    ),
]

TEAM2_ARGS = [
    (
        "The claim that AI destroys jobs fundamentally misunderstands economic history. "
        "Every industrial revolution displaced some jobs while creating far more. AI is "
        "projected to create 97 million new roles by 2025 — a net gain of 12 million "
        "jobs. The question is not whether jobs are lost but whether we invest in "
        "transition. "
        "(Source: https://www.weforum.org/reports/the-future-of-jobs-report-2020)"
    ),
    (
        "Surveillance misuse is a governance failure not a technology failure. The same "
        "facial recognition technology my opponent vilifies is being used to find missing "
        "children — over 3000 recovered in India in just four days using AI facial "
        "matching. We do not ban cars because some people drink and drive. "
        "(Source: https://timesofindia.indiatimes.com/india/facial-recognition-system-helps-"
        "trace-3000-missing-children-in-4-days/articleshow/63870129.cms)"
    ),
    (
        "AI in medicine is saving lives at a scale no human system could match. DeepMind's "
        "AlphaFold solved the 50-year protein folding problem in 2020, unlocking potential "
        "cures for Alzheimer's, Parkinson's, and cancer. One breakthrough of this magnitude "
        "outweighs the harms my opponent has described. "
        "(Source: https://www.nature.com/articles/s41586-021-03819-2)"
    ),
    (
        "In conclusion — my opponent argued against the misuse of AI by bad actors. I "
        "argued for the fundamental nature of AI as a tool that amplifies human capability. "
        "AlphaFold, medical diagnosis, climate modeling, educational access — these are not "
        "theoretical. They are happening now and they are helping billions. Harm comes from "
        "humans. Benefit comes from the technology itself. The motion falls."
    ),
]

TOPIC = "Artificial Intelligence will do more harm than good to society"
DESCRIPTION = (
    "Debate whether the overall impact of AI on humanity is net negative considering "
    "job displacement, misinformation, surveillance, and existential risk versus "
    "economic growth, medical advances, and productivity gains."
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def finish_time_ms(offset_ms: int = 900_000) -> int:
    return int(time.time() * 1000) + offset_ms


async def send(ws, payload: dict):
    raw = json.dumps(payload)
    await ws.send(raw)
    msg_type = payload.get("type", "?")
    preview = raw[:120]
    log.info("SENT  [%s] %s", msg_type, preview)


def make_match_state(status: str, turn: str, remaining_ms: int = 900_000) -> dict:
    return {
        "type": "match-state",
        "from": "system",
        "timestamp": get_timestamp(),
        "data": {
            "team1": "TEAM ALPHA",
            "team2": "TEAM BETA",
            "topic": TOPIC,
            "description": DESCRIPTION,
            "round": "Round 1",
            "finishTime": finish_time_ms(remaining_ms),
            "pros": "team1",
            "cons": "team2",
            "turn": turn,
            "status": status,
            "remainingTime": remaining_ms,
        },
    }


# ---------------------------------------------------------------------------
# Match simulation
# ---------------------------------------------------------------------------


async def run_match(ws):
    # Step 1 — welcome
    await send(ws, {
        "type": "welcome",
        "from": "system",
        "timestamp": get_timestamp(),
        "data": {"message": "Welcome to Agent SLAM Mock Server!"},
    })

    # Step 2 — match-state (active)
    await asyncio.sleep(2)
    await send(ws, make_match_state("active", "team1"))

    # Step 3 — match-update
    await asyncio.sleep(2)
    await send(ws, {
        "type": "match-update",
        "from": "system",
        "timestamp": get_timestamp(),
        "data": {
            "message": "The match has started! Let the slam begin! It's team1's turn.",
            "finishTime": finish_time_ms(),
        },
    })

    # Step 4 — match-state (started)
    await send(ws, make_match_state("started", "team1"))

    # Step 5 — debate loop (8 messages total, 4 per team)
    await asyncio.sleep(5)

    current_turn = "team1"
    t1_idx = 0
    t2_idx = 0
    remaining = 900_000

    for _ in range(8):
        await asyncio.sleep(4)
        remaining -= 60_000  # simulate ~60s passing per exchange

        if current_turn == "team1":
            await send(ws, {
                "type": "debate-message",
                "from": "team1",
                "timestamp": get_timestamp(),
                "data": {"message": TEAM1_ARGS[t1_idx]},
            })
            t1_idx += 1
            next_turn = "team2"
        else:
            await send(ws, {
                "type": "debate-message",
                "from": "team2",
                "timestamp": get_timestamp(),
                "data": {"message": TEAM2_ARGS[t2_idx]},
            })
            t2_idx += 1
            next_turn = "team1"

        await asyncio.sleep(1)
        await send(ws, make_match_state("started", next_turn, remaining))
        current_turn = next_turn

    # Step 6 — match-finish
    await asyncio.sleep(3)
    await send(ws, {
        "type": "match-finish",
        "from": "system",
        "timestamp": get_timestamp(),
        "data": {"message": "The match has ended!"},
    })

    # Step 7 — keep open then close
    log.info("Match finished. Keeping connection open for 10s...")
    await asyncio.sleep(10)


# ---------------------------------------------------------------------------
# Connection handler
# ---------------------------------------------------------------------------


async def handler(ws):
    log.info("Client connected from %s", ws.remote_address)

    match_task = asyncio.create_task(run_match(ws))

    try:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                log.warning("Received non-JSON: %s", raw[:100])
                continue

            msg_type = msg.get("type", "unknown")

            if msg_type == "debate-message":
                text = msg.get("data", {}).get("message", "")
                log.info("AGENT SENT: %s", text[:100])
                # acknowledge
                await send(ws, {
                    "type": "info",
                    "from": "system",
                    "timestamp": get_timestamp(),
                    "data": {"message": "acknowledged"},
                })
            else:
                log.info("RECV  [%s] %s", msg_type, raw[:120])
    except websockets.ConnectionClosed:
        log.info("Client disconnected")
    finally:
        match_task.cancel()
        try:
            await match_task
        except asyncio.CancelledError:
            pass


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main():
    log.info("Starting mock server on ws://localhost:%d", PORT)
    async with websockets.serve(handler, "localhost", PORT):
        log.info("Mock server ready — waiting for connections...")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Server stopped.")
