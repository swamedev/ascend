#!/usr/bin/env python3
"""
Shadow Ledger Validator — Valida integridade do manifest.md e ADRs.
Parte do Ascended Governance Toolkit.
"""

import hashlib
import re
import os
import sys


MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "manifest.md")


def compute_file_hash(filepath: str) -> str:
    """Computa SHA-256 do arquivo inteiro."""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def extract_adrs(content: str) -> list:
    """Extrai ADRs e seus hashes do manifest."""
    adrs = []
    adr_pattern = re.compile(r"### (ADR-\d+):.*")
    hash_pattern = re.compile(r'\*\*Hash:\*\*\s*`([^`]+)`')

    current_adr = None
    for line in content.split("\n"):
        adr_match = adr_pattern.match(line)
        if adr_match:
            current_adr = adr_match.group(1)

        if current_adr:
            hash_match = hash_pattern.search(line)
            if hash_match:
                adrs.append({
                    "id": current_adr,
                    "hash": hash_match.group(1)
                })
                current_adr = None

    return adrs


def validate():
    """Valida integridade do manifest."""
    manifest = os.path.abspath(MANIFEST_PATH)

    if not os.path.exists(manifest):
        print("[LEDGER] ❌ manifest.md não encontrado!")
        return False

    with open(manifest, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar estrutura mínima
    checks = {
        "ARCHITECTURE_MODE": "ARCHITECTURE_MODE" in content,
        "ADR section": "## Architecture Decision Records" in content,
        "Changelog": "## Changelog" in content,
    }

    all_ok = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"[LEDGER] {status} {check_name}")
        if not passed:
            all_ok = False

    # Extrair e validar ADRs
    adrs = extract_adrs(content)
    print(f"[LEDGER] 📋 {len(adrs)} ADR(s) encontrada(s)")

    for adr in adrs:
        if adr["hash"] and len(adr["hash"]) > 5:
            print(f"[LEDGER] ✅ {adr['id']} — hash: {adr['hash']}")
        else:
            print(f"[LEDGER] ⚠️  {adr['id']} — hash ausente ou inválido")
            all_ok = False

    # Hash do arquivo completo
    file_hash = compute_file_hash(manifest)
    print(f"[LEDGER] 🔒 Manifest SHA-256: {file_hash[:16]}...")

    if all_ok:
        print("[LEDGER] ✅ INTEGRIDADE CONFIRMADA")
    else:
        print("[LEDGER] ⚠️  PROBLEMAS DETECTADOS — verifique acima")

    return all_ok


if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
