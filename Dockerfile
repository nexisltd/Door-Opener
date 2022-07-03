FROM python:3.10.4-bullseye

EXPOSE 8000

RUN apt update

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY /src/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY /src /app
COPY entrypoint.sh /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
ENTRYPOINT ["sh", "entrypoint.sh"]