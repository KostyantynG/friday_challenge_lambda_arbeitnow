import json
import requests
import boto3

url = "https://www.arbeitnow.com/api/job-board-api"
s3_client = boto3.client('s3')
bucket = "lambda-arbeitnow-challenge"

def get_raw_jobs():    
    response = requests.get(url)
    return response.json()["data"]

def get_jobs_list():
    raw_jobs = get_raw_jobs()
    jobs_list = []
    for job_api in raw_jobs:
        jobs_list.append({
            "id": job_api["slug"],
            "title": job_api["title"],
            "description": job_api["description"]
        })
    return jobs_list

jobs_list = get_jobs_list()

def upload_job(job):
    job_string = json.dumps(job)
    job_bytes = str.encode(job_string)
    s3_client.put_object(
        Body = job_bytes,
        Bucket = bucket,
        Key = job["id"] + ".json"
    )

def upload_jobs(jobs):
    for job in jobs:
        upload_job(job)

upload_jobs(jobs_list)
