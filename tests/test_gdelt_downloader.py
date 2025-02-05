import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
import psycopg2

from gdelt_downloader import GDELTDownloader
from config import DATA_DIR, DB_CONFIG
from db_schema import EVENTS_SCHEMA, MENTIONS_SCHEMA, GKG_SCHEMA

@pytest.fixture
def mock_downloader():
    """Fixture to create a GDELTDownloader instance with mocked dependencies"""
    with patch('gdelt_downloader.requests') as mock_requests, \
         patch('gdelt_downloader.psycopg2.connect') as mock_db:
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        downloader = GDELTDownloader()
        yield downloader, mock_requests, mock_conn, mock_cur

def test_setup_directories(tmp_path, mock_downloader):
    """Test directory creation"""
    downloader, _, _ = mock_downloader
    downloader._setup_directories()
    assert DATA_DIR.exists()

def test_create_tables(mock_downloader):
    """Test table creation"""
    downloader, _, mock_db = mock_downloader
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn

    downloader._create_tables()

    # Verify table creation calls
    for schema in [EVENTS_SCHEMA, MENTIONS_SCHEMA, GKG_SCHEMA]:
        mock_conn.execute.assert_any_call(
            f"CREATE TABLE IF NOT EXISTS {schema.name} ({', '.join(schema.columns)})"
        )

def test_get_master_file(mock_downloader):
    """Test master file download"""
    downloader, mock_requests, _ = mock_downloader
    mock_response = MagicMock()
    mock_response.text = "line1\nline2\nline3"
    mock_requests.get.return_value = mock_response

    result = downloader.get_master_file()

    mock_requests.get.assert_called_once_with("http://data.gdeltproject.org/gdeltv2/masterfilelist.txt")
    assert result == ["line1", "line2", "line3"]

def test_process_file_skips_invalid(mock_downloader):
    """Test that invalid file lines are skipped"""
    downloader, _, _ = mock_downloader
    downloader._get_file_type = MagicMock(return_value=None)

    downloader.process_file("invalid line")

    downloader._get_file_type.assert_not_called()

def test_download_file_exists(mock_downloader, tmp_path):
    """Test that existing files aren't re-downloaded"""
    downloader, mock_requests, _ = mock_downloader
    test_file = tmp_path / "test.csv"
    test_file.touch()

    downloader._download_file("http://example.com/test.csv", test_file)

    mock_requests.get.assert_not_called()

def test_process_csv(mock_downloader, tmp_path):
    """Test CSV processing"""
    downloader, _, _ = mock_downloader
    test_file = tmp_path / "test.csv"
    test_file.write_text("col1\tcol2\nval1\tval2")

    mock_conn = MagicMock()
    downloader.conn = mock_conn

    downloader._process_csv(test_file, "test_table")

    mock_conn.execute.assert_called_with("INSERT INTO test_table SELECT * FROM chunk")

def test_run_completes(mock_downloader):
    """Test the main run method completes"""
    downloader, mock_requests, _ = mock_downloader
    mock_response = MagicMock()
    mock_response.text = "line1\nline2\nline3"
    mock_requests.get.return_value = mock_response

    downloader.process_file = MagicMock()

    downloader.run()

    mock_requests.get.assert_called_once()
    assert downloader.process_file.call_count == 3

def test_database_connection_closed(mock_downloader):
    """Test that database connection is closed"""
    downloader, _, mock_db = mock_downloader
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn

    downloader.run()

    mock_conn.close.assert_called_once()

@pytest.mark.parametrize("url,expected", [
    ("http://example.com/export.csv", "events"),
    ("http://example.com/mentions.csv", "mentions"),
    ("http://example.com/gkg.csv", "gkg"),
    ("http://example.com/other.csv", None)
])
def test_get_file_type(mock_downloader, url, expected):
    """Test file type detection"""
    downloader, _, _ = mock_downloader
    result = downloader._get_file_type(url)
    assert result == expected
