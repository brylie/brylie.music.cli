# Brylie's Music CLI (`brylie-music-cli`)

A Python CLI tool designed to streamline the management of music production projects, specifically focusing on automating task creation and organization within GitHub Projects.

## Project Overview

This project aims to provide a wizard-style interface to set up music release projects (Albums, EPs, Singles, Videos). It utilizes predefined task templates and maps them to GitHub Project fields such as Category, Priority, and Phase.

**Key Technologies:**

* **Language:** Python 3.14
* **Package/Environment Manager:** `uv`
* **CLI Framework:** `click`
* **Data Modeling:** `pydantic`
* **Testing:** `pytest`
* **External Dependencies:** `gh` (GitHub CLI) for API interactions.

## Architecture

The codebase is organized into modular components:

* **`src/main.py`**: The main entry point for the CLI application. Currently contains a basic `wizard` command.
* **`src/models.py`**: Contains comprehensive Pydantic models defining:
  * `Task`: The structure of a task, including CLI-specific metadata and GitHub Project fields.
  * `ReleaseConfig`: User configuration for a specific release.
  * `GitHubProjectFields`: Definitions for custom fields in GitHub Projects (Category, Priority, Phase).
  * `ReleaseType`, `Category`, `Priority`, `Phase`: Enums for standardization.
* **`src/tasks.py`**: Intended for task filtering and management logic (currently a stub).
* **`src/github.py`**: Intended for interactions with the GitHub API via the `gh` CLI (currently a stub).
* **`data/tasks.json`**: JSON file intended to store the database of task templates (currently empty).

## Building and Running

The project uses `uv` for command execution and environment management.

### Prerequisites

* Python 3.14+
* `uv`
* `gh` (GitHub CLI) - Required for future GitHub integration features.

### Commands

**Run the CLI:**
To run the main CLI wizard:

```bash
uv run python src/main.py wizard
```

**Run Tests:**
To execute the test suite:

```bash
uv run pytest
```

## Development Conventions

* **Dependency Management:** All dependencies are managed via `pyproject.toml` and `uv.lock`. Use `uv` commands to add/remove dependencies.
* **Code Structure:** Keep models, logic, and interface separated.
  * `models.py` for data structures.
  * `tasks.py` for business logic.
  * `github.py` for external API calls.
* **Testing:** Write tests in the `tests/` directory using `pytest`.
* **Type Safety:** Leverage Pydantic for robust data validation and type checking.
