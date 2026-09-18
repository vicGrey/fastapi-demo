# fastapi-demo

A small FastAPI service with a Docker-based CI/CD pipeline that validates data before an image can be built or published, not just as a separate check afterward.
## What this does

Most CI setups validate data as a step alongside the build. This project bakes validation into the build itself. The Docker builder stage runs the validation script as part of docker build, so a bad dataset fails the build, not just a later pipeline check.## Pipeline flow

```
push to main
     │
     ▼
GitHub Actions: checkout, install deps, syntax check
     │
     ▼
validate_files.sh   → required files exist? (schema.json, data.json)
     │
     ▼
validate_data.py     → data matches schema.json (via jsonschema)
     │
     ▼
docker build          → builder stage re-runs validation before copying
     │                  the venv into the final image
     ▼
docker push → ghcr.io/vicgrey/fastapi-demo
```

If validation fails at any point, the pipeline stops. No image is built or published.

## Validation

- **`schema.json`** : defines required fields, types, and whether extra fields are allowed, using JSON Schema.
- **`validate_data.py`** : validates `data.json` against `schema.json` using Python's `jsonschema` library. Raises on failure (non-zero exit).
- **`validate_files.sh`** : confirms required files exist before anything else runs, so validation doesn't fail trying to parse a missing file.

## Docker

- **Multi-stage build**: dependencies are installed into a venv in the builder stage, then only that venv is copied into the runner stage — so build tools never ship in the final image.
- **Validation runs inside the build**: the builder stage validates data before the runner stage is even built, so `docker build` itself fails on bad data — not just CI.
- **`LABEL` metadata** on the final image records `version`, `schema`, and `source`, so an image can be inspected (`docker inspect`) without tracing back through commit history.

## Running it locally

```bash
# build (validation runs as part of this)
docker build -t fastapi-demo .

# run
docker run -p 8000:8000 fastapi-demo
```

To see the fail-fast behavior, break `data.json` (remove a required field or change a type) and re-run `docker build` — the build fails before an image is produced.

## Known limitations / next steps

This is a learning project, and these are gaps I'm aware of, not blind spots:

- **Image tagging is static** (`:1.0`), so every build to `main` overwrites the same tag. Next step: tag by Git commit SHA for traceability.
- **No non-root user** in the runner stage yet — the container currently runs as root.
- **No image vulnerability scanning** (e.g. Trivy) integrated into the pipeline yet.
- **Validation is single-file** — `validate_data.py` checks one `data.json` against one schema; it doesn't yet handle a directory of records.
- **No `LABEL` build-date or Git-SHA metadata yet** — only static version/schema/source labels.

## Stack

Python, FastAPI, Docker (multi-stage builds), GitHub Actions, JSON Schema, GitHub Container Registry (GHCR)
