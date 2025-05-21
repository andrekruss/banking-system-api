FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ARG PORT=80

EXPOSE ${PORT}

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]