# AI Job Hunter

An intelligent job hunting assistant that automatically scrapes job listings, analyzes them using AI, and helps you find the most relevant opportunities.

## Features

- **Job Scraping**: Automatically fetches job listings from differnet listing boards.
- **AI Analysis**: Uses OpenAI to analyze job listings for:
  - Remote work compatibility
  - Job relevance
  - European location compatibility
- **SQLite Storage**: Efficiently stores and manages job listings
- **Real-time Updates**: Continuously monitors for new job opportunities
- **Web Interface**: View and manage job listings through a web browser

### Job boards
Currently supported job boards:
- [RemoteOK](https://remoteok.com/) - ✅ Remote jobs from around the world
- [GolangProjects](https://golangprojects.com/) - 🚧 Coming soon!

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
cp .env.example .env
```
Then add your OpenAI key and model you want to use.

## Usage

### Running the Complete System

You can run all components using the unified `main.py` script:

```bash
# Run all components (scraper, analyzer, and web interface)
python main.py --all

# Run specific components
python main.py --scraper --analyzer  # Run scraper and analyzer
python main.py --web                 # Run just the web interface

# Enable debug logging
python main.py --all --debug
```

### Individual Components

#### Scraping Jobs

To fetch new job listings:
```bash
python scraper.py
```

#### Analyzing Jobs

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

#### Web Interface

To start the web interface:
```bash
python list.py
```

The web interface will be available at `http://localhost:5000`

## Project Structure

- `scrape/`: Job scraping modules
  - `providers/`: Job board scrapers
  - `models.py`: Data models
- `store/`: Database management
  - `sqlite.py`: SQLite storage implementation
- `analyze/`: AI analysis modules
- `scraper.py`: Main scraping script
- `analyzer.py`: Main analysis script
- `list.py`: Web interface script
- `main.py`: Unified system launcher

## License

[MIT](LICENSE)


