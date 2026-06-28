import subprocess
import os
import sys

with open("install_log.txt", "w") as f:
    print("Installing backend dependencies...")
    res = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=r"e:\Projects\GenesisWeb-AI\backend", stdout=f, stderr=f)
    print("Backend install code:", res.returncode)

    print("Installing frontend dependencies...")
    # On Windows, use shell=True and npm directly
    res2 = subprocess.run("npm install", cwd=r"e:\Projects\GenesisWeb-AI\frontend", stdout=f, stderr=f, shell=True)
    print("Frontend install code:", res2.returncode)

print("Check install_log.txt for details.")
