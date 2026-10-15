# Harvester Lambda

Harvester is an AWS Lambda function that takes a URL and returns the sentences it considers important. A browser extension highlights those strings on the page.

This is the backend for the Web Harvester project from CMPE 295B, built by Arun Ram, Pranav Prem, Renu Parameshwaran, and Suchita Mudholkar. The extension is the [`WebHighlighter`](https://github.com/SuchitaM/WebHighlighter-Frontend) submodule.

## What you get back

`service.handler` accepts an event like this:

```json
{"url": "https://en.wikipedia.org/wiki/Real_Madrid_C.F."}
```

It returns a JSON list of strings. It does not return an API Gateway proxy payload (`statusCode` and `body`). The 2018 integration passed the list through as the response body, and the extension iterates that array.

A fragment is returned only when it occurs verbatim in the ASCII-stripped HTML. `html2text` inserts line breaks, so on many real pages the list is empty. That check is the original filter.

## Architecture

```text
event["url"]
  sentence_engine
    fetch the page with urllib and drop non-ASCII characters
    convert HTML to text with html2text
    split on periods
    drop lines of 5 characters or fewer, and lines that contain * or |
    keep terms that occur more than 5 times, at most 20 of them
    build a count matrix, one row per remaining line
  SMMRY
    score each row by the sum of its cosine similarities to every row
    take the ten highest scores
    split those lines on punctuation and keep pieces longer than 30 characters
  handler
    keep a piece only when it is a substring of the fetched HTML
```

Three other rankers are in the tree and are not called. `CNN.py` is a partial MNIST tutorial. `regressor.py` is a Bayesian ridge model over Reddit comment scores whose training file and Reddit client were never connected. `ensemble.py` is an empty constructor. The 2018 handler named all three and then raised `NameError` before returning anything. The handler now runs the path that was actually implemented.

## Tech stack

| Piece | Choice |
| --- | --- |
| Language | Python 3.12 or newer. Local checks run on 3.12. |
| Lambda runtime | `python3.14` (`python3.12` and `python3.13` are also supported on Lambda) |
| HTML to text | `html2text` 2025.4.15 (GPL-3.0-or-later) |
| Tokenizing and stopwords | `nltk` 3.10.3 (Apache-2.0) |
| Tests and lint | pytest 9.1.1, Ruff 0.17.0 |
| Region / function | `us-west-1`, function name `harvester`, handler `service.handler`, timeout 35 seconds |

This repository does not have a license file. `html2text` is GPL-3.0-or-later, which matters if you ship a bundle that includes it.

`boto3` is not installed into the zip. The Lambda runtime provides it, and the function code does not call AWS APIs.

## Project structure

```text
lambda_function/
  service.py                  handler
  sentence_engine.py          fetch, tokenize, count matrix
  SMMRY.py                    cosine ranking
  StemmedCountVectorizer.py   stemmer for the unfinished regressor
  regressor.py                unfinished Reddit-score model
  CNN.py                      unfinished MNIST paste
  ensemble.py                 unfinished combiner
  config.yaml                 region, runtime, timeout, environment
  event.json                  sample event
  nltk_data/                  English stopwords and punkt_tab
scripts/package_lambda.sh     build the deployment zip
tests/                        unit tests, no network
.github/workflows/ci.yml      ruff and pytest on Python 3.12 and 3.14
WebHighlighter/               browser-extension submodule
pyproject.toml                project metadata and tool settings
requirements.txt              pinned runtime dependencies for the zip
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

cd lambda_function
python service.py event.json
```

`event.json` points at a Wikipedia page, so that command makes a network request. From the repo root, the same call is:

```bash
PYTHONPATH=lambda_function python lambda_function/service.py lambda_function/event.json
```

NLTK data is bundled under `lambda_function/nltk_data`. NLTK 3.10 refuses a data directory that another account can write to, including `/tmp`, so keep custom downloads in a private directory such as `~/nltk_data`.

## Test

```bash
pytest
ruff check .
ruff format --check .
```

The tests mock `urlopen`. They do not fetch live pages.

## Deploy

The `python-lambda` CLI this repo used in 2018 is archived and is not a dependency. Packaging is a zip of the function modules, the pinned libraries, and `nltk_data`:

```bash
./scripts/package_lambda.sh
```

The zip is written to `lambda_function/dist/harvester.zip` (gitignored).

Update an existing function with the AWS credential chain (environment variables, `~/.aws/credentials`, or a role):

```bash
aws lambda update-function-code \
  --region us-west-1 \
  --function-name harvester \
  --zip-file fileb://lambda_function/dist/harvester.zip

aws lambda update-function-configuration \
  --region us-west-1 \
  --function-name harvester \
  --runtime python3.14 \
  --handler service.handler \
  --timeout 35 \
  --environment "Variables={NLTK_DATA=./nltk_data}"
```

Creating the function requires an execution role you already have:

```bash
aws lambda create-function \
  --region us-west-1 \
  --function-name harvester \
  --runtime python3.14 \
  --handler service.handler \
  --timeout 35 \
  --role arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME \
  --zip-file fileb://lambda_function/dist/harvester.zip \
  --environment "Variables={NLTK_DATA=./nltk_data}"
```

The function fetches whatever URL it is given. On a role with broad network access, that includes internal addresses. Put it behind the caller you intend, and give the role only the permissions it needs.

## Configuration

`lambda_function/config.yaml` records the deploy settings: region, function name, handler, runtime, timeout, and `NLTK_DATA`.

`aws_access_key_id` and `aws_secret_access_key` are present and empty on purpose. Leave them empty. Credentials belong in the AWS credential chain, never in this file. Nothing in the repository is a filled-in secret.

## WebHighlighter

`WebHighlighter` is a gitlink to [SuchitaM/WebHighlighter-Frontend](https://github.com/SuchitaM/WebHighlighter-Frontend) at the commit recorded in 2018. The parent repo did not include `.gitmodules`, so the link did not check out. It does now.

```bash
git submodule update --init WebHighlighter
```

The extension posts `{"url": "<current page>"}` to API Gateway and highlights each string in the JSON array. That frontend is not modified here.
