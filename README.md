# philiprehberger-env-file

[![Tests](https://github.com/philiprehberger/py-env-file/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-env-file/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-env-file.svg)](https://pypi.org/project/philiprehberger-env-file/)
[![License](https://img.shields.io/github/license/philiprehberger/py-env-file)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

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

- `load_env(*paths, override=True)` — Load .env files into `os.environ`, returns dict of loaded vars
- `parse_env_file(path)` — Parse a .env file, returns dict without modifying environment


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
