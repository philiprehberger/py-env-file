# Changelog

## 0.2.0 (2026-05-30)

- Add `dump_env()` for writing dicts to .env files with quoting
- Add `merge_env()` for parsing multiple .env files into a single dict without touching `os.environ`

## 0.1.6- Standardize README structure and fix compliance issues
## 0.1.5- Add pytest and mypy tool configuration to pyproject.toml

## 0.1.5 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.4

- Add Development section to README

## 0.1.1

- Add project URLs to pyproject.toml

## 0.1.0 (2026-03-10)

- Initial release
- .env file parsing with comment support
- Variable interpolation with \ syntax
- Multi-file loading with override priority
- Parse without modifying os.environ
