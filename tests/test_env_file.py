import os
import tempfile
from pathlib import Path

import pytest
from philiprehberger_env_file import dump_env, load_env, merge_env, parse_env_file


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


def test_dump_env_roundtrip(tmp_path: Path):
    data = {"FOO": "bar", "BAZ": "qux"}
    out = tmp_path / "out.env"
    dump_env(data, out)
    assert parse_env_file(str(out)) == data


def test_dump_env_quotes_whitespace(tmp_path: Path):
    out = tmp_path / "out.env"
    dump_env({"FOO": "value with space"}, out)
    text = out.read_text(encoding="utf-8")
    assert 'FOO="value with space"' in text
    assert parse_env_file(str(out)) == {"FOO": "value with space"}


def test_dump_env_roundtrip_embedded_quotes(tmp_path: Path):
    out = tmp_path / "out.env"
    data = {"FOO": 'a "quoted" b'}
    dump_env(data, out)
    assert parse_env_file(str(out)) == data


def test_dump_env_invalid_key_raises(tmp_path: Path):
    with pytest.raises(ValueError):
        dump_env({"BAD KEY": "x"}, tmp_path / "out.env")


def test_dump_env_creates_parent_dirs(tmp_path: Path):
    out = tmp_path / "nested" / "sub" / "out.env"
    dump_env({}, out)
    assert out.is_file()


def test_merge_env_later_overrides_earlier(tmp_path: Path):
    f1 = tmp_path / "a.env"
    f2 = tmp_path / "b.env"
    f1.write_text("FOO=one\nBAR=keep\n", encoding="utf-8")
    f2.write_text("FOO=two\nBAZ=new\n", encoding="utf-8")
    assert merge_env(f1, f2) == {"FOO": "two", "BAR": "keep", "BAZ": "new"}


def test_merge_env_missing_path_returns_empty(tmp_path: Path):
    assert merge_env(tmp_path / "does-not-exist.env") == {}


def test_merge_env_does_not_touch_environ(tmp_path: Path):
    f1 = tmp_path / "a.env"
    f2 = tmp_path / "b.env"
    f1.write_text("MERGE_ENV_TEST_KEY=one\n", encoding="utf-8")
    f2.write_text("MERGE_ENV_TEST_KEY=two\n", encoding="utf-8")
    assert "MERGE_ENV_TEST_KEY" not in os.environ
    merge_env(f1, f2)
    assert "MERGE_ENV_TEST_KEY" not in os.environ
