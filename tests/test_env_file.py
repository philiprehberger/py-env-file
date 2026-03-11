import os
import tempfile
from pathlib import Path

import pytest
from philiprehberger_env_file import load_env, parse_env_file


def _write_env(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False)
    f.write(content)
    f.close()
    return f.name


def test_parse_basic():
    path = _write_env("KEY=value\nNAME=Alice\n")
    result = parse_env_file(path)
    assert result == {"KEY": "value", "NAME": "Alice"}
    os.unlink(path)


def test_parse_export_prefix():
    path = _write_env("export KEY=value\n")
    result = parse_env_file(path)
    assert result == {"KEY": "value"}
    os.unlink(path)


def test_parse_comments():
    path = _write_env("# comment\nKEY=value\n")
    result = parse_env_file(path)
    assert result == {"KEY": "value"}
    os.unlink(path)


def test_parse_double_quotes():
    path = _write_env('KEY="hello world"\n')
    result = parse_env_file(path)
    assert result == {"KEY": "hello world"}
    os.unlink(path)


def test_parse_single_quotes():
    path = _write_env("KEY='hello world'\n")
    result = parse_env_file(path)
    assert result == {"KEY": "hello world"}
    os.unlink(path)


def test_parse_empty_value():
    path = _write_env("KEY=\n")
    result = parse_env_file(path)
    assert result == {"KEY": ""}
    os.unlink(path)


def test_parse_inline_comment():
    path = _write_env("KEY=value # comment\n")
    result = parse_env_file(path)
    assert result == {"KEY": "value"}
    os.unlink(path)


def test_interpolation():
    path = _write_env("BASE=hello\nFULL=${BASE}_world\n")
    result = parse_env_file(path)
    assert result["FULL"] == "hello_world"
    os.unlink(path)


def test_load_env_sets_environ():
    path = _write_env("TEST_LOAD_KEY=test_value_123\n")
    load_env(path)
    assert os.environ.get("TEST_LOAD_KEY") == "test_value_123"
    del os.environ["TEST_LOAD_KEY"]
    os.unlink(path)


def test_load_env_no_override():
    os.environ["EXISTING_KEY"] = "original"
    path = _write_env("EXISTING_KEY=new_value\n")
    load_env(path, override=False)
    assert os.environ["EXISTING_KEY"] == "original"
    del os.environ["EXISTING_KEY"]
    os.unlink(path)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_env_file("/nonexistent/.env")


def test_escape_sequences_in_double_quotes():
    path = _write_env('KEY="line1\\nline2"\n')
    result = parse_env_file(path)
    assert result["KEY"] == "line1\nline2"
    os.unlink(path)
