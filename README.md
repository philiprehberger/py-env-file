# philiprehberger-env-file

[![Tests](https://github.com/philiprehberger/py-env-file/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-env-file/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-env-file.svg)](https://pypi.org/project/philiprehberger-env-file/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-env-file)](https://github.com/philiprehberger/py-env-file/commits/main)

.env file parser with interpolation and multi-file support.

## Installation

```bash
pip install philiprehberger-env-file
```

## Usage

### Load into Environment

```python
from philiprehberger_env_file import load_env

# Load .env (default)
load_env()

# Load multiple files (later files override earlier)
load_env(".env", ".env.local")

# Don't override existing env vars
load_env(override=False)
```

### Parse Without Modifying Environment

```python
from philiprehberger_env_file import parse_env_file

config = parse_env_file(".env")
print(config["DATABASE_URL"])
```

### Writing .env files

```python
from philiprehberger_env_file import dump_env

dump_env(
    {"DATABASE_URL": "postgres://localhost/db", "DEBUG": "1"},
    ".env",
)
```

Values containing whitespace, ``#``, ``"``, or ``'`` are automatically
quoted. Pass ``quote=False`` to disable.

### Merging without loading

```python
from philiprehberger_env_file import merge_env

# Later files override earlier ones; os.environ is untouched
config = merge_env(".env", ".env.local")
```

### Supported Syntax

```bash
# Comments
KEY=value
export KEY=value

# Quoted values
SINGLE='no interpolation here'
DOUBLE="supports\nnewlines"

# Variable interpolation
BASE_URL=https://api.example.com
API_URL=${BASE_URL}/v1

# Empty values
EMPTY_VAR=

# Inline comments (unquoted values only)
HOST=localhost # this is a comment
```

## API

| Function / Class | Description |
|------------------|-------------|
| `load_env(*paths, override=True)` | Load .env files into `os.environ`, returns dict of loaded vars |
| `parse_env_file(path)` | Parse a .env file, returns dict without modifying environment |
| `dump_env(data, path, quote=True)` | Write a dict to a .env file, auto-quoting values that need it |
| `merge_env(*paths)` | Parse multiple .env files into one dict; missing files are skipped, `os.environ` is not modified |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-env-file)

🐛 [Report issues](https://github.com/philiprehberger/py-env-file/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-env-file/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
