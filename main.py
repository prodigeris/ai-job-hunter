import json
from scrape.scraper import Scraper
from scrape.providers.remoteok import RemoteOKScraper

def main():
    # Initialize scraper with list of providers
    scraper = Scraper([RemoteOKScraper])
    
    # Fetch jobs from all providers
    jobs = scraper.fetch_all_jobs()

    print(f"\nFound {len(jobs)} total jobs:")
    for job in jobs:
        print(f"\nURL: {job.url}")
        print(f"Published: {job.published_at}")
        print(f"Content: {job.content[:200]}...")

    jobs_data = [
        {
            "url": str(job.url),
            "content": job.content,
            "published_at": job.published_at.isoformat(),
            "created_at": job.created_at.isoformat(),
            "checksum": job.checksum
        }
        for job in jobs
    ]

    with open("output.json", "w") as f:
        json.dump(jobs_data, f, indent=2)

    print(f"\nSaved {len(jobs)} jobs to output.json")

if __name__ == "__main__":
    main()
