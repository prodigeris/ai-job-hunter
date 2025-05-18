import time
from datetime import datetime, UTC
from store.sqlite import SQLiteStore
from analyze.models import AnalyzedJob
from analyze.openai import analyze_job_listing

class JobAnalyzer:
    def __init__(self, store: SQLiteStore):
        self.store = store

    def analyze_job(self, job) -> AnalyzedJob:
        """Mock analysis of a job. In reality, this would use NLP/AI to analyze the content."""
        return AnalyzedJob(
            job_listing_id=job.id,
            url=job.url,
            salary_from=job.salary_min,
            salary_to=job.salary_max,
            is_remote_score=0.8 if 'remote' in job.content.lower() else 0.2,
            is_applicable_score=0.7,  # Mock score
            is_european_score=0.6 if job.location and any(c in job.location.lower() for c in ['europe', 'eu', 'uk', 'germany', 'france', 'spain', 'italy']) else 0.3,
            analyzed_at=datetime.now(UTC),
            title=job.title
        )

    def run(self, poll_interval: int = 60):
        """Continuously poll for unanalyzed jobs and analyze them."""
        print(f"Starting job analyzer. Polling every {poll_interval} seconds...")
        
        while True:
            try:
                unanalyzed_jobs = self.store.get_unanalyzed_jobs()
                
                if unanalyzed_jobs:
                    print(f"Found {len(unanalyzed_jobs)} unanalyzed jobs")
                    for job in unanalyzed_jobs:
                        print(f"Analyzing job: {job.url}")
                        analysis = self.analyze_job(job)
                        if self.store.save_analysis(analysis):
                            print(f"Analysis complete and saved: remote={analysis.is_remote_score:.2f}, applicable={analysis.is_applicable_score:.2f}, european={analysis.is_european_score:.2f}")
                        else:
                            print(f"Failed to save analysis for job: {job.url}.")
                            
                    print(f"Completed analysis of {len(unanalyzed_jobs)} jobs")
                else:
                    print("No new jobs to analyze")
                
                time.sleep(poll_interval)
                
            except Exception as e:
                print(f"Error during analysis: {str(e)}")
                time.sleep(poll_interval)
