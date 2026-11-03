"""Minimal example: run the seek-jobs-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "country": "AU",
    "keyword": "software engineer",
    "location": "All-Sydney-NSW",
    "maxItems": 50,
}

run = client.actor("bibian/seek-jobs-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    count += 1
    print(f"{item['title']} | {item.get('companyName')} | {item.get('locationLabel')} | {item.get('salaryMin')}-{item.get('salaryMax')} {item.get('salaryCurrency') or ''}")
print(f"{count} results")
