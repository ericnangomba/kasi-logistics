# System Manifest

## Project Overview
- Name: kasi-logistics
- Description: CRCT-enabled project: kasi-logistics
- Created: 2026-10-27T07:48:30.800Z

## Current Status
- Current Phase: Set-up/Maintenance
- Last Updated: 2026-11-10T16:45:03.950Z

## Project Structure

- 1000 py files


## Dependencies

## Project Directory Structure

- 📂 app/
  - 📂 __pycache__/
    - 📄 __init__.cpython-312.pyc
    - 📄 main.cpython-312.pyc
    - 📄 security.cpython-312.pyc
  - 📂 agent/
    - 📂 __pycache__/
      - 📄 __init__.cpython-312.pyc
      - 📄 optimizer.cpython-312.pyc
      - 📄 paymerch.cpython-312.pyc
      - 📄 spatial.cpython-312.pyc
    - 📄 __init__.py
    - 📄 optimizer.py
    - 📄 paymerch.py
    - 📄 spatial.py
  - 📄 __init__.py
  - 📄 main.py
  - 📄 run_local.sh
  - 📄 security.py
- 📂 kasi_logistics.egg-info/
  - 📄 dependency_links.txt
  - 📄 PKG-INFO
  - 📄 SOURCES.txt
  - 📄 top_level.txt
- 📂 static/
  - 📄 index.html
- 📂 tests/
  - 📂 __pycache__/
    - 📄 test_api.cpython-312-pytest-9.2.0.pyc
  - 📄 test_api.py
- 📄 pyproject.toml
- 📄 requirements.txt
- 📄 run.py


## PY Dependencies

### \app\__init__.py
No dependencies found

### \app\security.py
Dependencies:
- os
- secrets
- time
- collections
- defaultdict
- asyncio
- Semaphore
- fastapi
- HTTPException,
- fastapi.security
- HTTPBearer,

### \app\main.py
Dependencies:
- logging
- pathlib
- Path
- fastapi
- FastAPI,
- fastapi.staticfiles
- StaticFiles
- fastapi.responses
- FileResponse
- fastapi.middleware.cors
- CORSMiddleware
- app.security
- verify_token,
- app.agent.spatial
- SAM31SpatialSegmenter,
- app.agent.optimizer
- (
- app.agent.paymerch
- router

### \run.py
Dependencies:
- uvicorn

### \tests\test_api.py
Dependencies:
- pytest
- fastapi.testclient
- TestClient
- app.main
- app



## Project Directory Structure





## Key Components
- TBD

## Integration Points
- TBD

## Technical Considerations
- TBD

## Implementation Notes
- TBD
