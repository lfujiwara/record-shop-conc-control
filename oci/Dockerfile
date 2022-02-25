FROM python:3.10-alpine as base

WORKDIR /app
COPY .. .
RUN pip install -r requirements.txt

FROM base AS development
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0",  "--reload"]

FROM base AS production
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0"]
