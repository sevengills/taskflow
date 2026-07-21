# ---------- Builder ----------
FROM python:3.13-slim AS builder

ENV VENV_PATH=/opt/venv

RUN python -m venv ${VENV_PATH}

ENV PATH="${VENV_PATH}/bin:$PATH"

WORKDIR /app

COPY requirements ./requirements

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements/base.txt

# ---------- Runtime ----------
FROM python:3.13-slim

ENV VENV_PATH=/opt/venv
ENV PATH="${VENV_PATH}/bin:$PATH"

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

COPY --from=builder ${VENV_PATH} ${VENV_PATH}

COPY app app
COPY alembic alembic
COPY alembic.ini .

RUN chown -R app:app /app

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]