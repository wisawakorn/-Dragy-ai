import subprocess
from pathlib import Path

repo = Path(r"C:\Users\Pornchai M\dragy-ai")
out_path = repo / "git_push_result.txt"

commands = [
    ["git", "status", "--short"],
    ["git", "add", "main.py", "requirements.txt"],
    ["git", "commit", "-m", "Upgrade AI UI and add real-model response support"],
    ["git", "push", "origin", "main"],
]

with out_path.open("w", encoding="utf-8") as f:
    for cmd in commands:
        f.write(f"$ {' '.join(cmd)}\n")
        result = subprocess.run(cmd, cwd=repo, text=True, capture_output=True)
        if result.stdout:
            f.write(result.stdout)
        if result.stderr:
            f.write(result.stderr)
        f.write(f"\n[exit={result.returncode}]\n")
        f.write("-" * 60 + "\n")
