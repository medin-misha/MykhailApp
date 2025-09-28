FROM ghcr.io/astral-sh/uv:python3.13-bookworm

LABEL creator = "@medin-misha"

COPY pyproject.toml .
COPY app app/
WORKDIR app/
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]