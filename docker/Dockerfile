FROM python:3.13-slim

WORKDIR /app

COPY ../pyproject.toml .
RUN pip install -e .

COPY ../src/ ./src/

CMD ["uvicorn", "src.jis.main:app", "--host", "0.0.0.0", "--port", "8000"]
