import argparse
from scrape.scraper import Scraper
from scrape.providers.remoteok import RemoteOKScraper
from store.sqlite import SQLiteStore

def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Job Scraper - Fetch job listings from various providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run scraper with default settings
  python scraper.py

  # Run scraper with debug logging
  python scraper.py --debug
        """
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    
    print("Starting Job Scraper...")
    print("-" * 50)
    
    try:
        # Initialize scraper with list of providers
        scraper = Scraper([RemoteOKScraper])
        store = SQLiteStore()
        
        # Fetch jobs from all providers
        jobs = scraper.fetch_all_jobs()

        print(f"\nFound {len(jobs)} total jobs:")
        stored_count = 0
        for job in jobs:
            print(f"\nURL: {job.url}")
            print(f"Published: {job.published_at}")
            print(f"Content: {job.content[:200]}...")
            
            # Store job in database
            if store.insert_job(job):
                stored_count += 1

        print(f"\nStored {stored_count} new jobs in database")
        return 0
        
    except KeyboardInterrupt:
        print("\nStopping scraper...")
        return 0
    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
