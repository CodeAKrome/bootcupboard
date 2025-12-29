#!/usr/bin/env python
import requests
import json

# Specify the search term
query = '"generative ai"'

# Define the API endpoint URL
url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"

# Define the query parameters
# citationCount:desc
# publicationDate:desc
query_params = {
    "query": '"generative ai"',
    "fields": "title,url,publicationTypes,publicationDate,openAccessPdf",
    "year": "2025-",
    "sort": "citationCount:desc"
}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
# api_key = "your api key goes here"  # Replace with the actual API key

# Define headers with API key
# headers = {"x-api-key": api_key}

# Send the API request
# response = requests.get(url, params=query_params, headers=headers).json()
response = requests.get(url, params=query_params).json()

print(f"Will retrieve an estimated {response['total']} documents")
retrieved = 0

# Write results to json file and get next batch of results
with open(f"papers.json", "a") as file:
    while True:
        if "data" in response:
            retrieved += len(response["data"])
            print(f"Retrieved {retrieved} papers...")
            for paper in response["data"]:
                print(json.dumps(paper), file=file)
        # checks for continuation token to get next batch of results
        if "token" not in response:
            break
        response = requests.get(f"{url}&token={response['token']}").json()

print(f"Done! Retrieved {retrieved} papers total")