# Energy Management System

## Usage

### Docker

### Venv

I used [uv](https://docs.astral.sh/uv/) package manager to handle dependencies.

After you install the tool, just run `uv sync` which will create venv.

Then you can use `uv run` to execute a python script or module.

## Development

Please install [pre-commit](https://pre-commit.com/) tool: `pip install pre-commit` (or `uv tool install pre-commit`)

Then install defined hooks from `.pre-commit-config.yaml` via `pre-commmit install`.

When you commit, your code will be checked by linter and then formatted (by [ruff](https://docs.astral.sh/ruff/)).

You can also run the hooks manually for all files with `pre-commit run --all-files`. 

## Description

### Improvements
* Add `device_type` table, so we have general device types.
* Add `relationship()` to SQL models (but honestly I don't like it).
* Add `device_metric` table, so we can have general metric types in `metric` table.
