# Session 2: Building Resilient AI Architectures

This project demonstrates a reusable Python structure for building resilient AI agent workflows using:

- dataclasses for structured agent configuration
- JSON persistence with safe file I/O
- resilient mock API error handling
- reusable code in the `src` package
- notebook-based experimentation

## Project Structure

- `app.py` - entry point that initializes the agent and runs the demo flow
- `src/agent_core.py` - reusable agent profile and resilience logic
- `src/` - reusable Python modules for the project
- `notebooks/` - step-wise notebooks for each lab concept
- `pyproject.toml` - packaging configuration for editable installs and builds

## Setup

1. Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

2. Install the project in editable mode:

```powershell
python -m pip install -e .
```

3. Install notebook support if needed:

```powershell
python -m pip install ipykernel
```

## Run the App

```powershell
python app.py
```

## Build the Package

```powershell
python -m build
```

## Notebook Usage

Open the notebooks in the `notebooks/` folder to explore each step:

- `step2_persistence_demo.ipynb`
- `step3_resilience_demo.ipynb`

## Notes

- The virtual environment is excluded from version control via `.gitignore`.
- The reusable logic lives in `src/` so it can be imported from both the app and notebooks.
- The project uses a packaging-based workflow so imports work cleanly after editable installation.
