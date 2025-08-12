FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

COPY . .

RUN poetry install --no-interaction --no-ansi
#dev group이 있다면 --without dev 옵션 추가

ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "python", "-m", "mcp_map_server.server"]