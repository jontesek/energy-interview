# Energy Management System

## Usage

Please first insert sample data to DB with this command:

`uv run -m energy_manager.db.insert_sample_data`

You can run tests with `uv run pytest`. Tests use local SQLite DB file named `energy_test.db` which is recreated on each run with sample data.

### Venv

I used [uv](https://docs.astral.sh/uv/) package manager to handle dependencies.

After you install the tool, just run `uv sync` which will create venv.

Then you can use `uv run` to execute a python script or module.

## Development

Please install [pre-commit](https://pre-commit.com/) tool: `pip install pre-commit` (or `uv tool install pre-commit`)

Then install hooks defined in `.pre-commit-config.yaml` via `pre-commmit install`.

When you commit, your code will be checked by linter and then formatted (by [ruff](https://docs.astral.sh/ruff/)).

You can also run the hooks manually for all files with `pre-commit run --all-files`. 

## Description

### Possible improvements
* Add `device_type` table, so we have general device types.
* Add `relationship()` to SQL models (but honestly I don't like it).
* Add `device_metric` table, so we can have general metric types in `metric` table.
* Instead of `X-User-ID` header use JWT token with `user_id` encrypted in it.
* Add user access check for `metrics` endpoints (I removed it to simplify development).
* DI using FastAPI `Depends()` doesn't allow db_url argument - rework it to make it more explicit (e.g. using [this](https://python-dependency-injector.ets-labs.org/)) library.
* Add endpoint to read values from metric subscription.
