import os
from pathlib import Path

# Base configuration
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "gdelt.db"

# GDELT URLs
MASTER_FILE_URL = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
BASE_DOWNLOAD_URL = "http://data.gdeltproject.org/gdeltv2/"

# File types to process
FILE_TYPES = {
    "events": "export",
    "mentions": "mentions",
    "gkg": "gkg"
}

# Database settings
CHUNK_SIZE = 100000  # Number of rows to process at a time
