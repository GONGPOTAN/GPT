FROM python:3.13.2 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt

FROM python:3.13.2-slim

WORKDIR /app

COPY --from=builder /app/.venv .venv/
COPY . .

# ✅ 가상환경을 시스템 PATH에 추가
ENV PATH="/app/.venv/bin:$PATH"

# ✅ main.py 실행
CMD ["python", "main.py"]