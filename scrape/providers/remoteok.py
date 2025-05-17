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

            # Parse salary range if available
            salary_str = item.get("salary", "")
            salary_min = None
            salary_max = None
            if salary_str:
                try:
                    # Remove currency symbols and 'k' suffix, convert to float
                    salary_clean = salary_str.replace("$", "").replace("k", "000")
                    if "-" in salary_clean:
                        min_str, max_str = salary_clean.split("-")
                        salary_min = float(min_str.strip())
                        salary_max = float(max_str.strip())
                    else:
                        salary_val = float(salary_clean)
                        salary_min = salary_max = salary_val
                except (ValueError, TypeError):
                    pass

            job = JobListing(
                url=item.get("url", ""),
                content=item.get("description", ""),
                published_at=datetime.fromtimestamp(timestamp, UTC),
                created_at=datetime.now(UTC),
                location=item.get("location"),
                salary_min=salary_min,
                salary_max=salary_max
            )
            jobs.append(job)

        print(f"Successfully fetched {len(jobs)} jobs", flush=True)
        return jobs
