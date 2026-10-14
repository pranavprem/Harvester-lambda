# Agent guide

Harvester is a Python AWS Lambda function. `service.handler` fetches `event["url"]` and returns a list of important sentence fragments. The full human-facing description is `README.md`. This file is the coding-agent briefing: architecture, conventions, commands, and traps.

## Architecture

The only path the handler runs:

1. `sentence_engine` downloads the URL, drops non-ASCII characters, converts HTML to text with `html2text`, and splits on `.`.
2. It drops lines of length 5 or less and lines containing `*` or `|`.
3. It builds a bag of at most 20 terms that each occur more than 5 times, then a count matrix with one row per kept line.
4. `SMMRY` scores each row by the sum of cosine similarities against every row, keeps the ten highest, splits those strings on any character that is not a letter or a space, and drops pieces of length 30 or less.
5. The handler returns the pieces that occur verbatim in the ASCII-stripped HTML.

`CNN.py`, `regressor.py`, and `ensemble.py` are unfinished experiments. Do not import them from `service.py`. Wiring them back in crashes the handler: `CNN` is a MNIST tutorial with undefined names, `regressor.get_important_sentences` returns a dict and reads an undefined file and Reddit client, and `ensemble` stores nothing.

The Lambda return value is a bare list of strings, not an API Gateway proxy response.

## Layout

Code that ships in the zip lives in `lambda_function/` as top-level modules (`service.handler`, not `lambda_function.service.handler`). Tests import them via `pythonpath = ["lambda_function"]` in `pyproject.toml`.

`lambda_function/nltk_data/` is runtime data: the 2018 English stopword list and the English `punkt_tab` tables. `scripts/package_lambda.sh` copies `lambda_function/*.py`, `requirements.txt`, and that data directory into the zip.

`WebHighlighter/` is a submodule (see `.gitmodules`). Leave it alone unless the task is the extension.

## Conventions

- Python 3.12 or newer. The Lambda runtime in `config.yaml` is `python3.14`.
- Runtime dependency pins live in both `pyproject.toml` `[project].dependencies` and `requirements.txt`. Those two lists must match. A test checks that.
- Dev tools (`pytest`, `ruff`) are only in `[project.optional-dependencies]`. Do not put them in the Lambda zip.
- Ruff selects `E`, `F`, `I`, and `UP`. `CNN.py` and `regressor.py` ignore undefined-name findings because those files are unfinished.
- Historical class names stay as they are: `sentence_engine`, `SMMRY`, `ensemble`, `regressor`. A rename is an API change for anyone importing them.
- Preserve ranking behavior. That includes the `prev` index in `SMMRY.get_important_sentences`, which is not reset for each sentence, and the handler's verbatim-HTML filter.
- Tests must not call the network. Patch `sentence_engine.urllib.request.urlopen`.
- Do not commit secrets, `.env` files, virtualenvs, `MLenv/`, or `lambda_function/dist/`.

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
cd lambda_function && python service.py event.json
```

`event.json` fetches a live Wikipedia URL. Deploy steps are in `README.md`. CI (`.github/workflows/ci.yml`) runs Ruff and pytest on Python 3.12 and 3.14.

## Gotchas

- The substring filter compares `html2text` output with the raw HTML. Wrapping adds spaces, so a live page can legitimately return `[]`. Do not "fix" that by dropping the check unless the task is a behavior change.
- Sentence rows and matrix rows stay aligned because both follow the same dict. Build them in one pass if you touch `filter`.
- Bag columns follow set iteration order. Cosine similarity is invariant to a consistent column order. Do not sort one row and not the others.
- `nltk` 3.10 will not load data from a directory another account can write to. `/tmp` is one of those. The bundled directory is `lambda_function/nltk_data`, and the function also appends `/nltk_data` for the old zip layout. `NLTK_DATA=./nltk_data` is set in `config.yaml`.
- The old `punkt` pickles were removed. NLTK dropped pickle models (they were a code-execution risk). `word_tokenize` needs `tokenizers/punkt_tab/english`. The English stopword file is still the 2018 list; replacing it changes which tokens survive.
- `StemmedCountVectorizer` imports scikit-learn. scikit-learn, TensorFlow, and PRAW are not runtime dependencies. Importing `regressor` or `CNN` fails in a normal install.
- `config.yaml` has blank `aws_access_key_id` and `aws_secret_access_key` fields. Leave them blank. No filled-in credentials are in this repo.
- The handler will request any URL it is given, including internal ones, and `urlopen` follows redirects. Treat that as the current behavior.
- `python-lambda` is archived. Package with `scripts/package_lambda.sh`.
