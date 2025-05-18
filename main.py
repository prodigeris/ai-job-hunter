import argparse
import subprocess
import sys
import time
import os
from threading import Thread

def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Job Hunter - Complete job hunting system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all components
  python main.py --all

  # Run specific components
  python main.py --scraper --analyzer
  python main.py --web

  # Run with debug logging
  python main.py --all --debug
        """
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all components (scraper, analyzer, and web interface)"
    )
    
    parser.add_argument(
        "--scraper",
        action="store_true",
        help="Run the job scraper"
    )
    
    parser.add_argument(
        "--analyzer",
        action="store_true",
        help="Run the AI job analyzer"
    )
    
    parser.add_argument(
        "--web",
        action="store_true",
        help="Run the web interface"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser

def run_scraper(debug=False):
    cmd = ["python", "scraper.py"]
    if debug:
        cmd.append("--debug")
    subprocess.run(cmd)

def run_analyzer(debug=False):
    cmd = ["python", "analyzer.py"]
    if debug:
        cmd.append("--debug")
    subprocess.run(cmd)

def run_web():
    cmd = ["python", "list.py"]
    subprocess.run(cmd)

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    
    # If no specific components are selected, show help
    if not any([args.all, args.scraper, args.analyzer, args.web]):
        parser.print_help()
        return 1
    
    # Check for OpenAI API key if analyzer is being run
    if args.all or args.analyzer:
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY environment variable is not set")
            print("Please set it using: export OPENAI_API_KEY='your-api-key'")
            return 1
    
    print("Starting AI Job Hunter...")
    print("-" * 50)
    
    try:
        threads = []
        
        # Run scraper if requested
        if args.all or args.scraper:
            print("\nStarting Job Scraper...")
            scraper_thread = Thread(target=run_scraper, args=(args.debug,))
            scraper_thread.start()
            threads.append(scraper_thread)
        
        # Run analyzer if requested
        if args.all or args.analyzer:
            print("\nStarting AI Job Analyzer...")
            analyzer_thread = Thread(target=run_analyzer, args=(args.debug,))
            analyzer_thread.start()
            threads.append(analyzer_thread)
        
        # Run web interface if requested
        if args.all or args.web:
            print("\nStarting Web Interface...")
            web_thread = Thread(target=run_web)
            web_thread.start()
            threads.append(web_thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        return 0
        
    except KeyboardInterrupt:
        print("\nStopping all components...")
        return 0
    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
