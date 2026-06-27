import subprocess
import sys
from pathlib import Path

repo = Path(r"C:\Users\Pornchai M\dragy-ai")
commit_message = "Upgrade AI UI and add real-model response support"


def run(cmd, check=False):
    result = subprocess.run(cmd, cwd=repo, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result

print("[1/4] Checking repo status")
status = run(["git", "status", "--short"])
if status.returncode != 0:
    raise SystemExit(status.returncode)

print("[2/4] Staging files")
run(["git", "add", "main.py", "requirements.txt"], check=True)

print("[3/4] Creating commit")
commit = run(["git", "commit", "-m", commit_message])
if commit.returncode != 0 and "nothing to commit" not in commit.stderr.lower():
    if "author identity unknown" in commit.stderr.lower():
        run(["git", "config", "user.name", "wisawakorn"], check=True)
        run(["git", "config", "user.email", "your_email@gmail.com"], check=True)
        run(["git", "commit", "-m", commit_message], check=True)
    else:
        raise SystemExit(commit.returncode)

print("[4/4] Pushing to origin/main")
run(["git", "push", "origin", "main"], check=True)
print("Push completed successfully.")
