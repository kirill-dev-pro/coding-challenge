# Backend

## Setup

1. Install poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies

```bash
poetry install
```

## Run

```bash
poetry run uvicorn main:app --reload
```
