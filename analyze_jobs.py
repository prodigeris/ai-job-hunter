from analyze.analyzer import JobAnalyzer
from store.sqlite import SQLiteStore

def main():
    store = SQLiteStore()
    analyzer = JobAnalyzer(store)
    analyzer.run(poll_interval=60)  # Poll every 60 seconds

if __name__ == "__main__":
    main() 