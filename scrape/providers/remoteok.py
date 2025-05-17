import requests
from datetime import datetime, UTC
from .base import BaseScraper
from .models import JobListing

class RemoteOKScraper(BaseScraper):
    def fetch_jobs(self):
        print("Fetching jobs from RemoteOK API...", flush=True)
        res = requests.get("https://remoteok.com/api", timeout=30)
        data = res.json()

        jobs = []
        for item in data:
            if item.get("position") is None:
                continue

            # Parse the date string to timestamp
            date_str = item.get("date", "")
            try:
                timestamp = int(float(date_str)) if date_str else int(datetime.now().timestamp())
            except (ValueError, TypeError):
                timestamp = int(datetime.now().timestamp())

            job = JobListing(
                url=item.get("url", ""),
                content=item.get("description", ""),
                published_at=datetime.fromtimestamp(timestamp, UTC),
                created_at=datetime.now(UTC)
            )
            jobs.append(job)

        print(f"Successfully fetched {len(jobs)} jobs", flush=True)
        return jobs
