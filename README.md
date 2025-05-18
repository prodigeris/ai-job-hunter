# AI Job Hunter

An intelligent job hunting assistant that automatically scrapes job listings, analyzes them using AI, and helps you find the most relevant opportunities.

## Features

- **Job Scraping**: Automatically fetches job listings from RemoteOK
- **AI Analysis**: Uses OpenAI to analyze job listings for:
  - Remote work compatibility
  - Job relevance
  - European location compatibility
- **SQLite Storage**: Efficiently stores and manages job listings
- **Real-time Updates**: Continuously monitors for new job opportunities

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/prodigeris/ai-job-hunter.git
cd ai-job-hunter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Usage

### Scraping Jobsx

To fetch new job listings:
```bash
python scraper.py
```

### Analyzing Jobs

To analyze job listings using AI:
```bash
python analyzer.py
```

Options:
- `--poll-interval`: Set the interval (in seconds) between checks for new jobs (default: 60)
- `--debug`: Enable debug logging

Example:
```bash
python analyzer.py --poll-interval 30 --debug
```

## Project Structure

- `scrape/`: Job scraping modules
  - `providers/`: Job board scrapers
  - `models.py`: Data models
- `store/`: Database management
  - `sqlite.py`: SQLite storage implementation
- `analyze/`: AI analysis modules
- `scraper.py`: Main scraping script
- `analyzer.py`: Main analysis script

## License

MIT


