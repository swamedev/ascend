import hashlib
import uuid


def generate_id(prefix: str = "") -> str:
    raw = uuid.uuid4().hex
    short = hashlib.md5(raw.encode()).hexdigest()[:12]
    return f"{prefix}{short}" if prefix else short
