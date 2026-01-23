# Brylie's Music CLI

CLI for Brylie's music projects.

## Usage

All commands should be prefixed with `uv` if you have not activated the Python environment.

### Auth with GitHub

Add the required GitHub Projects scope to your authentication:

```sh
gh auth refresh -s project
```

### Run the CLI wizard

Prompt for first and last name, then echo them as a single string:

```sh
uv run python src/main.py wizard
```

### Run tests

Run the test suite using pytest:

```sh
uv run pytest
```
