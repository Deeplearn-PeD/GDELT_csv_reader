import os
from pathlib import Path

# Base configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

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
DB_CONFIG = {
    'dbname': 'gdelt_raw',
    'user': 'postgres',
    'password': 'eueueu',
    'host': 'localhost',
    'port': 5432
}
