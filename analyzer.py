import os
import argparse
from store.sqlite import SQLiteStore
from analyze.analyzer import JobAnalyzer

def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Job Analyzer - Analyze job listings using OpenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run analyzer with default settings (60s poll interval)
  python analyzer.py

  # Run analyzer with custom poll interval
  python analyzer.py --poll-interval 30

  # Run analyzer with debug logging
  python analyzer.py --debug
        """
    )
    
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=60,
        help="Interval in seconds between checking for new jobs (default: 60)"
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
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        print("Please set it using: export OPENAI_API_KEY='your-api-key'")
        return 1
    
    # Initialize store and analyzer
    store = SQLiteStore()
    analyzer = JobAnalyzer(store)
    
    print("Starting AI Job Analyzer...")
    print(f"Polling interval: {args.poll_interval} seconds")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        analyzer.run(poll_interval=args.poll_interval)
    except KeyboardInterrupt:
        print("\nStopping analyzer...")
        return 0
    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
