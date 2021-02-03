FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /transcribe-frontend
COPY requirements.txt /transcribe-frontend/
RUN pip install -r requirements.txt
COPY . /transcribe-frontend/

