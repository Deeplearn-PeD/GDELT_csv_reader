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
        "GLOBALEVENTID INTEGER",
        "SQLDATE INTEGER",
        "MonthYear INTEGER",
        "Year INTEGER",
        "FractionDate FLOAT",
        "Actor1Code TEXT",
        "Actor1Name TEXT",
        "Actor1CountryCode TEXT",
        "Actor1KnownGroupCode TEXT",
        "Actor1EthnicCode TEXT",
        "Actor1Religion1Code TEXT",
        "Actor1Religion2Code TEXT",
        "Actor1Type1Code TEXT",
        "Actor1Type2Code TEXT",
        "Actor1Type3Code TEXT",
        "Actor2Code TEXT",
        "Actor2Name TEXT",
        "Actor2CountryCode TEXT",
        "Actor2KnownGroupCode TEXT",
        "Actor2EthnicCode TEXT",
        "Actor2Religion1Code TEXT",
        "Actor2Religion2Code TEXT",
        "Actor2Type1Code TEXT",
        "Actor2Type2Code TEXT",
        "Actor2Type3Code TEXT",
        "IsRootEvent INTEGER",
        "EventCode TEXT",
        "EventBaseCode TEXT",
        "EventRootCode TEXT",
        "QuadClass INTEGER",
        "GoldsteinScale FLOAT",
        "NumMentions INTEGER",
        "NumSources INTEGER",
        "NumArticles INTEGER",
        "AvgTone FLOAT",
        "Actor1Geo_Type INTEGER",
        "Actor1Geo_FullName TEXT",
        "Actor1Geo_CountryCode TEXT",
        "Actor1Geo_ADM1Code TEXT",
        "Actor1Geo_ADM2Code TEXT",
        "Actor1Geo_Lat FLOAT",
        "Actor1Geo_Long FLOAT",
        "Actor1Geo_FeatureID TEXT",
        "Actor2Geo_Type INTEGER",
        "Actor2Geo_FullName TEXT",
        "Actor2Geo_CountryCode TEXT",
        "Actor2Geo_ADM1Code TEXT",
        "Actor2Geo_ADM2Code TEXT",
        "Actor2Geo_Lat FLOAT",
        "Actor2Geo_Long FLOAT",
        "Actor2Geo_FeatureID TEXT",
        "ActionGeo_Type INTEGER",
        "ActionGeo_FullName TEXT",
        "ActionGeo_CountryCode TEXT",
        "ActionGeo_ADM1Code TEXT",
        "ActionGeo_ADM2Code TEXT",
        "ActionGeo_Lat FLOAT",
        "ActionGeo_Long FLOAT",
        "ActionGeo_FeatureID TEXT",
        "DATEADDED INTEGER",
        "SOURCEURL TEXT"
    ],
    primary_key="GLOBALEVENTID"
)

MENTIONS_SCHEMA = TableSchema(
    name="mentions",
    columns=[
        "GLOBALEVENTID INTEGER",
        "EventTimeDate INTEGER",
        "MentionTimeDate INTEGER",
        "MentionType INTEGER",
        "MentionSourceName TEXT",
        "MentionIdentifier TEXT",
        "SentenceID INTEGER",
        "Actor1CharOffset INTEGER",
        "Actor2CharOffset INTEGER",
        "ActionCharOffset INTEGER",
        "InRawText INTEGER",
        "Confidence INTEGER",
        "MentionDocLen INTEGER",
        "MentionDocTone FLOAT",
        "MentionDocTranslationInfo TEXT",
        "Extras TEXT"
    ],
    primary_key="GLOBALEVENTID"
)

GKG_SCHEMA = TableSchema(
    name="gkg",
    columns=[
        "GKGRECORDID TEXT",
        "DATE INTEGER",
        "SourceCollectionIdentifier INTEGER",
        "SourceCommonName TEXT",
        "DocumentIdentifier TEXT",
        "Counts TEXT",
        "V2Counts TEXT",
        "Themes TEXT",
        "V2Themes TEXT",
        "Locations TEXT",
        "V2Locations TEXT",
        "Persons TEXT",
        "V2Persons TEXT",
        "Organizations TEXT",
        "V2Organizations TEXT",
        "V2Tone TEXT",
        "Dates TEXT",
        "GCAM TEXT",
        "SharingImage TEXT",
        "RelatedImages TEXT",
        "SocialImageEmbeds TEXT",
        "SocialVideoEmbeds TEXT",
        "Quotations TEXT",
        "AllNames TEXT",
        "Amounts TEXT",
        "TranslationInfo TEXT",
        "Extras TEXT"
    ],
    primary_key="GKGRECORDID"
)
