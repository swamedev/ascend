#!/usr/bin/env python3
"""
Replay Manifest — Reconstrói o estado do manifest a partir do arquivo de changelog.
Parte do Ascended Governance Toolkit.
"""

import os
import json
from datetime import datetime


MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "manifest.md")
REPLAY_LOG = os.path.join(os.path.dirname(__file__), "..", ".arsenal", "replay_log.jsonl")


def log_event(event_type: str, details: dict):
    """Registra evento no replay log."""
    os.makedirs(os.path.dirname(REPLAY_LOG), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": details
    }

    with open(REPLAY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[REPLAY] Evento registrado: {event_type}")


def replay():
    """Reproduz o log de eventos para auditoria."""
    if not os.path.exists(REPLAY_LOG):
        print("[REPLAY] Nenhum replay log encontrado. Iniciando log vazio.")
        log_event("INIT", {"message": "Replay log inicializado"})
        return

    with open(REPLAY_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"[REPLAY] {len(lines)} evento(s) no log:")
    print("-" * 60)

    for line in lines:
        try:
            entry = json.loads(line.strip())
            ts = entry.get("timestamp", "?")
            evt = entry.get("event", "?")
            details = entry.get("details", {})
            print(f"  [{ts}] {evt}: {json.dumps(details, ensure_ascii=False)}")
        except json.JSONDecodeError:
            print(f"  [ERRO] Linha corrompida: {line.strip()[:80]}")

    print("-" * 60)
    print("[REPLAY] Replay completo.")


if __name__ == "__main__":
    replay()
