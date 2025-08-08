# Repository Guidelines

## Project Structure & Modules
- `app/`: FastAPI service code.
  - `api/`: route handlers (`/api/v1`).
  - `core/`: domain logic (routing, ranking, generation, tool-calling).
  - `data/`: prompts, subsectors, context hints.
  - `routes/`: semantic routes and `routing_table.json`.
  - `utils/`: logging, IO helpers.
- `tests/`: Pytest suite (`test_*.py`, configured by `tests/pytest.ini`).
- `envs/`: environment files for local/dev/prod.
- Docker: `Dockerfile`, `docker-compose*.yml`.

## Build, Test, and Run
- Install: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Run API (local): `python -m app.main --env-file envs/.env.dev.local` (serves FastAPI on `HOST:PORT`).
- Health check: `curl http://localhost:8001/api/v1/health` (dev) or `:8000` (prod).
- Docker (prod): `docker compose up --build` (maps `8000:8000`).
- Docker (debug): `docker compose -f docker-compose.debug.yml up --build` (maps `8001:8000`, debug on `5678`).
- Tests: `pytest -q` or with coverage `pytest --cov=app --cov-report=term-missing`.

## Coding Style & Naming
- Python 3.12, PEP 8, 4-space indent, type hints required for new/changed code.
- Modules, files, variables: `snake_case`; classes: `PascalCase`; constants: `UPPER_SNAKE`.
- Keep APIs in `app/api`, business logic in `app/core`, data-only artifacts in `app/data`/`app/routes`.
- Use `app.utils.logger` for logging; avoid prints.

## Testing Guidelines
- Framework: Pytest. Tests live in `tests/`, files `test_*.py`, functions `test_*`.
- Unit-test services in `app/core` with fixtures/mocking; see examples in `tests/test_*`.
- Aim for coverage on changed lines; prefer deterministic tests (mock OpenAI calls as in fixtures).

## Commit & Pull Requests
- Conventional Commits: `feat(scope): …`, `fix(scope): …`, `docs: …`, `refactor: …` (see `git log`).
- PRs must include: purpose/summary, linked issue, test plan (commands, screenshots/cURL), and notes on env/config changes.
- Keep diffs focused; update/add tests with behavior changes.

## Security & Config
- Do not hardcode secrets. Use `--env-file` or `envs/.env.*` files (excluded from VCS).
- Default models/hosts are configured via env: `PROVIDER_BASE_URL`, `*_MODEL`, `HOST`, `PORT`, etc.
