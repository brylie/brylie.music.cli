# Brylie's Music CLI (`brylie-music-cli`)

A Python CLI tool designed to streamline the management of music production projects, specifically focusing on automating task creation and organization within GitHub Projects.

## Project Overview

This project provides a CLI to set up music release projects (Albums, EPs, Singles, Videos). It utilizes predefined task templates and maps them to GitHub Project fields such as Category, Priority, and Phase.

**Key Technologies:**

- **Language:** Python 3.14
- **Package/Environment Manager:** `uv`
- **CLI Framework:** `click`
- **Data Modeling:** `pydantic`
- **Testing:** `pytest`
- **External Dependencies:** `gh` (GitHub CLI) for API interactions.

## Architecture

The codebase is organized into modular components:

- **`src/main.py`**: Entry point. Contains CLI commands like `create-project` (automates project setup) and `wizard`.
- **`src/models.py`**: Pydantic models for `Task`, `ReleaseConfig`, `ProjectMetadata`, and Enums for GitHub fields (`Category`, `Priority`, `Phase`).
- **`src/tasks.py`**: Logic for loading and filtering tasks from the database.
- **`src/github.py`**: Wrapper around `gh` CLI to create projects, fields, and items, and update custom fields.
- **`data/tasks.json`**: JSON database containing the standard library of music production tasks.

## Building and Running

The project uses `uv` for command execution and environment management.

### Prerequisites

- Python 3.14+
- `uv`
- `gh` (GitHub CLI) - Authenticated and installed.

### Commands

**Create a Release Project:**
To create a new GitHub Project with automated tasks:

```bash
uv run python src/main.py create-project
```

**Run the Wizard:**
Basic wizard command:

```bash
uv run python src/main.py wizard
```

**Run Tests:**
To execute the test suite:

```bash
uv run pytest
```

## Development Conventions

- **Dependency Management:** Managed via `pyproject.toml` and `uv.lock`.
- **Code Structure:**
  - `models.py`: Data definitions and validation.
  - `tasks.py`: Task data handling.
  - `github.py`: API interactions.
- **Testing:** Tests in `tests/` using `pytest`.
- **Type Safety:** Use Pydantic models for data interchange.
