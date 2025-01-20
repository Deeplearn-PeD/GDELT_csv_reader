import os
import psycopg2
import psycopg2.extras
import requests
from requests.exceptions import HTTPError
import pandas as pd
from pathlib import Path
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import loguru

logger = loguru.logger

from config import (
    MASTER_FILE_URL,
    BASE_DOWNLOAD_URL,
    DATA_DIR,
    FILE_TYPES,
    CHUNK_SIZE,
    DB_CONFIG
)
from db_schema import EVENTS_SCHEMA, MENTIONS_SCHEMA, GKG_SCHEMA

class GDELTDownloader:
    def __init__(self):
        self._setup_directories()
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()
        self._create_tables()

    def _setup_directories(self):
        """Create required directories if they don't exist"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _create_tables(self):
        """Create database tables based on schemas"""
        for schema in [EVENTS_SCHEMA, MENTIONS_SCHEMA, GKG_SCHEMA]:
            create_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema.name} (
                    {', '.join(schema.columns)},
                    PRIMARY KEY ({schema.primary_key})
                )
            """
            self.cur.execute(create_sql)
        self.conn.commit()

    def get_master_file(self) -> List[str]:
        """Download and parse the master file list"""
        print("Downloading master file list...")
        response = requests.get(MASTER_FILE_URL)
        response.raise_for_status()
        return response.text.splitlines()

    def process_file(self, file_info: str):
        """Process a single GDELT file"""
        parts = file_info.split()
        if len(parts) < 3:
            return

        file_url = parts[2]
        file_type = self._get_file_type(file_url)
        if not file_type:
            return

        # Download and process the file
        local_path = DATA_DIR / Path(file_url).name
        try:
            self._download_file(file_url, local_path)
            self._process_csv(local_path, file_type)
        except HTTPError as e:
            logger.error(f"Error downloading {file_url}: {e}")

    def _get_file_type(self, file_url: str) -> Optional[str]:
        """Determine file type based on URL"""
        for key, pattern in FILE_TYPES.items():
            if pattern in file_url:
                return key
        return None

    def _download_file(self, url: str, local_path: Path):
        """Download a file with progress tracking"""
        if local_path.exists():
            return

        print(f"Downloading {url}...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def _process_csv(self, file_path: Path, table_name: str):
        """Process CSV file and insert into database"""
        logger.info(f"Processing {file_path.name}...")
        try:
            for chunk in pd.read_csv(
                file_path,
                sep='\t',
                header=None,
                chunksize=CHUNK_SIZE,
                low_memory=False
            ):
                # Convert DataFrame to list of tuples
                tuples = [tuple(x) for x in chunk.to_numpy()]
                
                # Generate the SQL query
                query = f"INSERT INTO {table_name} VALUES %s ON CONFLICT DO NOTHING"
                try:
                    psycopg2.extras.execute_values(
                        self.cur,
                        query,
                        tuples,
                        template=None,
                        page_size=int(CHUNK_SIZE/10)
                    )
                    self.conn.commit()
                except psycopg2.Error as e:
                    logger.error(f"Error processing chunk: {e}")
                    self.conn.rollback()  # Rollback the failed transaction
                    continue  # Skip to next chunk
        except Exception as e:
            logger.error(f"Error processing file {file_path.name}: {e}")
            self.conn.rollback()

    def run(self):
        """Main execution method"""
        try:
            files = self.get_master_file()
            with ThreadPoolExecutor() as executor:
                list(tqdm(executor.map(self.process_file, files), total=len(files)))
        finally:
            self.cur.close()
            self.conn.close()

if __name__ == "__main__":
    downloader = GDELTDownloader()
    downloader.run()
