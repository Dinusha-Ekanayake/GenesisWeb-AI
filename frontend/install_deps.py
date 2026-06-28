import subprocess
import os

cwd = r"e:\Projects\GenesisWeb-AI\frontend"
print(f"Running npm install in {cwd}")

try:
    # Use shell=True to allow resolving 'npm'
    process = subprocess.run(
        "npm install", 
        shell=True, 
        cwd=cwd, 
        capture_output=True,
        text=True
    )
    print("STDOUT:")
    print(process.stdout)
    if process.stderr:
        print("STDERR:")
        print(process.stderr)
        
    print(f"Return code: {process.returncode}")
except Exception as e:
    print(f"Error: {e}")
