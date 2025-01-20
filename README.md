# GDELT Data Downloader

A Python application to download GDELT datasets (Events, Mentions, and Global Knowledge Graph) and store them in a DuckDB database.

## Features
- Downloads GDELT data files in parallel
- Stores data in a local DuckDB database
- Processes large files in chunks for memory efficiency
- Supports Events, Mentions, and GKG datasets

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/gdelt-downloader.git
cd gdelt-downloader
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install duckdb pandas requests tqdm
```

## Usage

Run the downloader:
```bash
python gdelt_downloader.py
```

The application will:
1. Create a `data/` directory if it doesn't exist
2. Download the master file list from GDELT
3. Download and process all available files
4. Store the data in `data/gdelt.db`

## Configuration

Edit `config.py` to adjust:
- Database location
- Download directory
- Chunk size for processing
- File types to download

## Database Schema

The database contains three tables:
- `events`: GDELT Event data
- `mentions`: Media mentions of events
- `gkg`: Global Knowledge Graph data

You can query the database using DuckDB:
```python
import duckdb
conn = duckdb.connect('data/gdelt.db')
events = conn.execute("SELECT * FROM events LIMIT 10").fetchdf()
```

## Notes
- The initial download may take several hours depending on your internet connection
- The database can grow quite large (100+ GB) for full datasets
- Downloaded CSV files are kept in the `data/` directory for future reference
