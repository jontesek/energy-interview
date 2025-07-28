# Energy Management System

## Installation and usage

Run `docker-compose up` to start the app - it will be accessible at http://127.0.0.1:8000. See API documentation at http://127.0.0.1:8000/docs. 

**Note**: You must include `X-User-ID` header in most requests (apart from `/metrics`). Payload format is mentioned in the docs (Endpoint > Request body).

**Insert sample data** with: `docker-compose run app uv run -m energy_manager.db.insert_sample_data`

Check the **SQLite database** in `/energy.db`. When you delete the file and start the app again, a new blank one is created.

Run **tests** with `docker-compose run app uv run pytest`. Tests use local SQLite DB file named `energy_test.db` which is recreated on each run with sample data.

### Run with venv

I used [uv](https://docs.astral.sh/uv/) package manager to handle dependencies. 
After you install the tool, just run `uv sync` which will create venv.
Then you can use `uv run` to execute a Python script or module.

To run the API without docker: `uv run -m energy_manager.app`

## Development

Please install [pre-commit](https://pre-commit.com/) tool: `pip install pre-commit` (or `uv tool install pre-commit`)

Then install hooks defined in [.pre-commit-config.yaml](./.pre-commit-config.yaml) via `pre-commmit install`.

When you commit, your code will be checked by linter and then formatted (by [ruff](https://docs.astral.sh/ruff/)). Ruff settings are located in [pyproject.toml](./pyproject.toml).

You can also run the hooks manually for all files with `pre-commit run --all-files`. 

### Python version

The Python version required by this project is specified in field `requires-python` in [pyproject.toml](./pyproject.toml).

By default, the `uv` tool uses the `.python-version` file to determine which Python version to use when running `uv sync`.  If you remove this file, `uv` will use the latest Python version satisfying the `requires-python` constraint when creating the venv.

That's exactly what we want. We don't need to support older Python versions via a looser `requires-python` value: This would be necessary only if the project were a library intended for use in other Python projects (with potentially different Python versions).

## Description

I started with DB design and created SQLAlchemy models. Then I designed the API endpoints and started working with FastAPI to achieve the desired results.

I used SQLite for easier development and debugging. I used FastAPI because I worked with it before. I used uv package manager because I wanted to try something new.

I used [Repository](./energy_manager/db/repository.py) classes for DB access and main logic. This way, API routers don't contain too much code and I can use some common code (e.g. for user access).

I added a lot of tests to properly test the API. I added a [separate test](./tests/unit/test_repository.py) for user access method to make sure it works properly. When testing create and update, I checked only API response, not data in DB. But since I also tried it manually before and it works (data is added), it should be fine.

Access rights for API operations are based on two roles: `basic` (read-only) and `tech` (also write). I use `UserRole` enum defined in [DB models](./energy_manager/db/models.py) to compare required role with user role for given site in DB.

I used mostly positional arguments in method calls. Although keyword arguments are safer and more future-proof, I tried this bold move this time, because it's not for production and I don't like repeating words :D.

I wrote almost no docstrings...but hopefully code is still easy to understand!

And last but not least, I confess the code was written mostly by me. But of course, I used AI chat for help when needed.

ERD for database:

![ERD](./erd.png)

### Possible improvements
* Add `device_type` table, so we have general device types.
* Add `relationship()` to SQL models (but honestly I don't like it, but it's good for cascade delete).
* Add `device_metric` table, so we can have general metric types in `metric` table.
* Instead of `X-User-ID` header use JWT token with `user_id` encrypted in it.
* Add user access check for `metrics` endpoints (I removed it to simplify development).
* DI using FastAPI `Depends()` doesn't allow db_url argument - rework it to make it more explicit (e.g. using [this library](https://python-dependency-injector.ets-labs.org/)).
* Add endpoint to read values from metric subscription.
* Dockerfile: Use non-root user for better security (I couldn't make it work with `uv`).
* Tests: use in-memory SQLite or cleanup DB file after test run. Advantage is that now you can open DB file and check data.
