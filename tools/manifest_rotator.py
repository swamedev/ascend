#!/usr/bin/env python3
"""
Manifest Rotator — Rotaciona e arquiva versões anteriores do manifest.md.
Parte do Ascended Governance Toolkit.
"""

import shutil
import hashlib
import os
from datetime import datetime


MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "manifest.md")
ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "..", ".arsenal", "manifest_archive")


def compute_hash(filepath: str) -> str:
    """Computa SHA-256 do arquivo."""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rotate():
    """Arquiva a versão atual do manifest com timestamp e hash."""
    manifest = os.path.abspath(MANIFEST_PATH)
    if not os.path.exists(manifest):
        print("[ROTATOR] manifest.md não encontrado. Nada a rotacionar.")
        return

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    file_hash = compute_hash(manifest)[:12]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"manifest_{timestamp}_{file_hash}.md"
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)

    shutil.copy2(manifest, archive_path)
    print(f"[ROTATOR] Manifest arquivado: {archive_name}")
    print(f"[ROTATOR] Hash: {file_hash}")
    return archive_path


if __name__ == "__main__":
    rotate()
