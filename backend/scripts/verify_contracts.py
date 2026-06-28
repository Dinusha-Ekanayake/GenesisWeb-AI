import os
import sys
import json
import subprocess
from fastapi.testclient import TestClient

# Ensure root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from backend.app.main import app

def main():
    print("Generating OpenAPI schema...")
    client = TestClient(app)
    response = client.get("/openapi.json")
    if response.status_code != 200:
        print(f"Failed to fetch openapi.json: {response.text}")
        sys.exit(1)
        
    openapi_spec = response.json()
    spec_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "openapi.json"))
    
    with open(spec_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
        
    print("Generating TypeScript definitions...")
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../frontend"))
    generated_ts_path = os.path.join(frontend_dir, "src/app/dashboard/types/generated-api.ts")
    
    # We use npx openapi-typescript to generate types based on the spec
    try:
        subprocess.run(
            ["npx", "--yes", "openapi-typescript", spec_path, "-o", generated_ts_path],
            check=True,
            cwd=frontend_dir,
            shell=True # Shell=True required on Windows for npx
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate TypeScript definitions: {e}")
        sys.exit(1)
        
    print(f"Successfully generated TypeScript definitions at {generated_ts_path}")
    print("Contract verification passed. The OpenAPI spec is the single source of truth.")
    
    # Clean up the JSON spec as it's not needed after generation
    os.remove(spec_path)
    
if __name__ == "__main__":
    main()
