import requests
import json
import boto3

s3_client = boto3.client('s3')

url = "https://www.arbeitnow.com/api/job-board-api"
response = requests.get(url)
raw_data = response.json()
jobs_data = raw_data["data"]
job = jobs_data[0]
job_template = {
        "id": job['slug'],
        "title": job['title'],
        "description": job['description']
    }

for job in jobs_data:
    job_template = {
        "id": job['slug'],
        "title": job['title'],
        "description": job['description']
    }

    job_template_json = json.dumps(job_template)
      
    with open("job.txt", "w") as file:
        file.write(job_template_json)
        
    s3_client.upload_file('job.txt', 'lambda-arbeitnow-challenge', job_template['id'])

