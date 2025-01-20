from dataclasses import dataclass
from typing import List

@dataclass
class TableSchema:
    name: str
    columns: List[str]
    primary_key: str

# Define schemas based on GDELT metadata
EVENTS_SCHEMA = TableSchema(
    name="events",
    columns=[
        "GlobalEventID INTEGER",
        "Day DATE",
        "MonthYear INTEGER",
        "Year INTEGER",
        "FractionDate REAL",
        # ... add all columns from GDELT metadata
        "SOURCEURL TEXT"
    ],
    primary_key="GlobalEventID"
)

MENTIONS_SCHEMA = TableSchema(
    name="mentions",
    columns=[
        "GlobalEventID INTEGER",
        "EventTime DATE",
        "MentionTime DATE",
        # ... add all columns from GDELT metadata
        "MentionDocTone REAL"
    ],
    primary_key="GlobalEventID"
)

GKG_SCHEMA = TableSchema(
    name="gkg",
    columns=[
        "GKGRECORDID TEXT",
        "DATE DATE",
        "SourceCollectionIdentifier INTEGER",
        # ... add all columns from GDELT metadata
        "SOURCEURL TEXT"
    ],
    primary_key="GKGRECORDID"
)
