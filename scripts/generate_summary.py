import os
from pathlib import Path

BASE = Path(r"D:\ASCEND PROJECT")
EXCLUDE_DIRS = {".venv", ".git", ".pytest_cache", "__pycache__", ".github"}
EXCLUDE_FILES = {"desktop.ini", ".gitignore", "tmp_summary.py"}
TEXT_EXTENSIONS = {".py", ".md", ".toml", ".json", ".yaml", ".yml", ".cfg", ".txt", ".ini"}

def should_include(path: Path):
    parts = set(path.parts)
    if EXCLUDE_DIRS & parts:
        return False
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix in TEXT_EXTENSIONS:
        return True
    return False

def main():
    output = []
    output.append("# ASCEND PROJECT — Full Context\n")
    output.append("## Directory Structure\n")
    for p in sorted(Path(BASE).rglob("*")):
        if p.is_file() and should_include(p):
            rel = p.relative_to(BASE)
            output.append(f"- {rel}")

    output.append("\n\n## File Contents\n")
    for p in sorted(Path(BASE).rglob("*")):
        if p.is_file() and should_include(p):
            rel = p.relative_to(BASE)
            output.append(f"\n### {rel}\n")
            output.append("```" + ("python" if p.suffix == ".py" else "markdown" if p.suffix == ".md" else ""))
            try:
                content = p.read_text(encoding="utf-8")
                output.append(content)
            except Exception as e:
                output.append(f"[Error reading: {e}]")
            output.append("```")

    Path("SUMMARY_FOR_CHATGPT.md").write_text("\n".join(output), encoding="utf-8")
    print("Done! File saved as SUMMARY_FOR_CHATGPT.md")

if __name__ == "__main__":
    BASE = r"D:\ASCEND PROJECT"
    main()
