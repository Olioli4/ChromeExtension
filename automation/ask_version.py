import subprocess

version = input("Enter version number for this commit: ").strip()
if not version:
    print("No version entered. Aborting.")
    exit(1)

commit_message = f"Release version {version}"
try:
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"Successfully pushed with commit message: {commit_message}")
except subprocess.CalledProcessError as e:
    print("Git command failed:", e)
    exit(1)