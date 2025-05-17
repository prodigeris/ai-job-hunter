from typing import List, Type
from datetime import datetime, UTC
from hashlib import md5
from pydantic import BaseModel, HttpUrl
from providers import JobListing

class Scraper:
    def __init__(self, providers: List[Type]):
        """
        Initialize the scraper with a list of provider classes.
        
        Args:
            providers: List of provider classes that inherit from BaseScraper
        """
        self.providers = [provider() for provider in providers]

    def fetch_all_jobs(self) -> List[JobListing]:
        """
        Fetch jobs from all configured providers.
        
        Returns:
            List of JobListing objects from all providers
        """
        all_jobs = []
        
        for provider in self.providers:
            try:
                print(f"Fetching jobs from {provider.__class__.__name__}...")
                jobs = provider.fetch_jobs()
                all_jobs.extend(jobs)
                print(f"Successfully fetched {len(jobs)} jobs from {provider.__class__.__name__}")
            except Exception as e:
                print(f"Error fetching jobs from {provider.__class__.__name__}: {str(e)}")
                continue

        return all_jobs
