import csv
from pathlib import Path
from types import SimpleNamespace

import pytest
import trio

from holehe.core import RESULT_FIELDS, export_csv, launch_module


async def _failing_module(email, client, out):
    raise RuntimeError("module failed")


async def github(email, client, out):
    raise RuntimeError("module failed")


def test_launch_module_uses_function_name_for_unknown_domain():
    out = []

    trio.run(launch_module, _failing_module, "user@example.com", None, out)

    assert out == [{
        "name": "_failing_module",
        "domain": "_failing_module.com",
        "method": "None",
        "frequent_rate_limit": False,
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None,
    }]


def test_launch_module_keeps_known_domain():
    out = []

    trio.run(launch_module, github, "user@example.com", None, out)

    assert out[0]["name"] == "github"
    assert out[0]["domain"] == "github.com"
    assert out[0]["error"] is True


def test_export_csv_accepts_mixed_result_rows(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = [
        {
            "name": "adobe",
            "domain": "adobe.com",
            "method": "password recovery",
            "frequent_rate_limit": False,
            "rateLimit": False,
            "exists": False,
            "emailrecovery": None,
            "phoneNumber": None,
            "others": None,
        },
        {
            "name": "duolingo",
            "domain": "duolingo.com",
            "method": "None",
            "frequent_rate_limit": False,
            "rateLimit": False,
            "error": True,
            "exists": False,
            "emailrecovery": None,
            "phoneNumber": None,
            "others": None,
        },
    ]

    with pytest.raises(SystemExit):
        export_csv(data, SimpleNamespace(csvoutput=True), "user@example.com")

    result_file = next(Path(".").glob("holehe_*_results.csv"))
    with result_file.open(newline="", encoding="utf8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == RESULT_FIELDS
    assert len(rows) == 2
    assert rows[0]["name"] == "adobe"
    assert rows[0]["error"] == ""
    assert rows[1]["name"] == "duolingo"
    assert rows[1]["error"] == "True"
