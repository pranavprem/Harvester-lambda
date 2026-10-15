# Harvester Lambda

Read `AGENTS.md` before editing. It is the full briefing (architecture, conventions, commands, gotchas). `README.md` is the human-facing map. This file is the short card so the two stay aligned.

Harvester is an AWS Lambda function. `service.handler` in `lambda_function/service.py` fetches `event["url"]` and returns a list of sentence fragments. The working path is `sentence_engine` then `SMMRY`. `CNN.py`, `regressor.py`, and `ensemble.py` are unfinished and must not be imported by the handler.

## Commands

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

pytest
ruff check .
ruff format .
ruff format --check .
./scripts/package_lambda.sh
```

CI runs those checks on Python 3.12 and 3.14. The Lambda runtime in `lambda_function/config.yaml` is `python3.14`. Deploy steps are in `README.md`.

## Rules

- Keep `requirements.txt` identical to `[project].dependencies` in `pyproject.toml`.
- Tests patch `sentence_engine.urllib.request.urlopen`. They do not hit the network.
- Leave the ranking math, the `prev` index in `SMMRY.get_important_sentences`, and the verbatim-HTML filter alone unless the task is a behavior change.
- Leave class names (`sentence_engine`, `SMMRY`, `ensemble`, `regressor`) alone.
- `aws_access_key_id` and `aws_secret_access_key` in `config.yaml` stay blank. Never commit credentials, `.env` files, virtualenvs, `MLenv/`, or `lambda_function/dist/`.
- NLTK data stays in `lambda_function/nltk_data`. NLTK 3.10 refuses group- or world-writable directories such as `/tmp`.
- `WebHighlighter/` is a submodule. Do not edit it for Lambda work.
