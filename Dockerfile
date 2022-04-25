# syntax=docker/dockerfile:1

FROM python:3.10.4-slim-buster
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "python3", "-m" , "uvicorn", "--port", "8000", "main:app", "--host=0.0.0.0"]
