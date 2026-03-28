"""
start_test.py — launch a full interactive test session with one command

Starts:  tests/interactive_server.py  (WebSocket broker on localhost:8766)
         agent.py --sandbox           (bot, connects to localhost:8766)
Opens:   tests/interactive_dashboard.html  in your default browser

Usage:
  python start_test.py
  python start_test.py --topic "AI will replace all jobs" --pros team1 --cons Perplexity
  python start_test.py --topic "..." --pros Perplexity --cons team1

Press Ctrl+C to stop everything.
"""

import os
import signal
import subprocess
import sys
import time
import urllib.parse
import webbrowser
from pathlib import Path

ROOT = Path(__file__).parent


def parse_flag(args: list[str], flag: str) -> str:
    """Return the value after --flag in args, or empty string."""
    for i, arg in enumerate(args):
        if arg == flag and i + 1 < len(args):
            return args[i + 1]
    return ""


def main():
    # Collect any extra args to forward to agent.py (--topic, --pros, --cons)
    extra_args = sys.argv[1:]

    procs: list[subprocess.Popen] = []

    def cleanup(sig=None, frame=None):
        print("\n[start_test] Shutting down...")
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        for p in procs:
            try:
                p.wait(timeout=3)
            except Exception:
                pass
        print("[start_test] Done.")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # ── 1. Start interactive server ───────────────────────────────────────────
    print("[start_test] Starting interactive server on ws://localhost:8766 ...")
    server = subprocess.Popen(
        [sys.executable, str(ROOT / "tests" / "interactive_server.py")],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    procs.append(server)

    # Wait for server to be ready
    time.sleep(1.5)

    if server.poll() is not None:
        print("[start_test] ERROR: interactive_server.py failed to start.")
        sys.exit(1)

    # ── 2. Open dashboard in browser with topic/stance pre-filled ────────────
    dashboard = ROOT / "tests" / "interactive_dashboard.html"
    topic = parse_flag(extra_args, "--topic")
    pros  = parse_flag(extra_args, "--pros")
    # Build query string so the dashboard can pre-fill its form
    params = {}
    if topic:
        params["topic"] = topic
    if pros:
        params["pros"] = pros
    uri = dashboard.as_uri()
    if params:
        uri += "?" + urllib.parse.urlencode(params)
    print(f"[start_test] Opening dashboard: {uri}")
    webbrowser.open(uri)

    # ── 3. Start agent in sandbox mode ────────────────────────────────────────
    agent_cmd = [sys.executable, str(ROOT / "agent.py"), "--sandbox"] + extra_args
    print(f"[start_test] Starting agent: {' '.join(agent_cmd)}")
    agent = subprocess.Popen(
        agent_cmd,
        stdout=sys.stdout,
        stderr=sys.stderr,
        cwd=str(ROOT),
    )
    procs.append(agent)

    # ── 4. Wait — keep running until Ctrl+C or agent exits ───────────────────
    try:
        agent.wait()
    except KeyboardInterrupt:
        pass

    cleanup()


if __name__ == "__main__":
    main()
