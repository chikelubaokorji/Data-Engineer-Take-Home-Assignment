FROM python:3.8

# Create working directory for this docker run scripts
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY etl/ /etl
COPY database/ /database

ENTRYPOINT ["python", "/etl/jobs_requests.py"]
