"""Repo hygiene that does not need the network or AWS."""

import ast
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_lambda_modules_parse():
    for path in sorted((ROOT / "lambda_function").glob("*.py")):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_runtime_pins_match_pyproject():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    required = [
        line.strip()
        for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert required == project["project"]["dependencies"]


def test_config_runtime_and_blank_credentials():
    text = (ROOT / "lambda_function" / "config.yaml").read_text(encoding="utf-8")
    assert "runtime: python3.14" in text
    for line in text.splitlines():
        if line.startswith(("aws_access_key_id:", "aws_secret_access_key:")):
            assert line.strip().endswith(":")


def test_package_script_syntax():
    script = ROOT / "scripts" / "package_lambda.sh"
    subprocess.run(["bash", "-n", str(script)], check=True)


def test_no_tracked_secret_markers():
    """The function config must not grow a filled-in access key."""
    blob = (ROOT / "lambda_function" / "config.yaml").read_text(encoding="utf-8")
    assert "AKIA" not in blob
