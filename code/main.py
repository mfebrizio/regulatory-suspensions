# Initialize
from pathlib import Path

from federal_register_api import query_endpoint_documents, query_endpoint_agencies, AgencyMetadata
from preprocessing import clean_agencies_column, column_to_date, clean_president_column
from utils import load_json, save_json, load_csv, save_csv


# create directories
p = Path(__file__)
raw_dir = p.parents[1].joinpath("data", "raw")
processed_dir = p.parents[1].joinpath("data", "processed")
analysis_dir = p.parents[1].joinpath("data", "analysis")
for dir in (raw_dir, processed_dir, analysis_dir):
    if not dir.exists():
        try:
            dir.mkdir(parents=True)
        except:
            print(f"Cannot create data directory: {dir}.")

# set constants
YEARS_RANGE = range(1994, 2023)
FILE_ALL_DATA_RAW = fr"documents_endpoint_{YEARS_RANGE[0]}_{YEARS_RANGE[-1]}.json"
FILE_AGENCIES_METADATA = r"agencies_endpoint_metadata.json"
FILE_ALL_DATA_PROCESSED =  fr"documents_endpoint_{YEARS_RANGE[0]}_{YEARS_RANGE[-1]}.csv"


def retrieve_documents(years, override_existing = False):
    """Retrieve and save documents from Federal Register API.
    """
    # check if already retrieved
    # don't make requests unless override is True or file does not exist
    file_path = raw_dir / FILE_ALL_DATA_RAW
    if override_existing or not file_path.is_file():
        # retrieve data from API
        documents = query_endpoint_documents(years)

        # --------------------------------------------------
        # export json file
        save_json(documents, FILE_ALL_DATA_RAW, raw_dir)

        # -------------------------------------------------- 
        # retrieve agencies metadata (for preprocessing)
        agencies_response = query_endpoint_agencies()
        agencies_metadata = AgencyMetadata(agencies_response)
        agencies_metadata.transform()
        agencies_metadata.save_json()


def process_documents():
    """
    """
    pass
    # Load data
    df = load_json(FILE_ALL_DATA_RAW, raw_dir)  # federal register documents
    agencies_metadata = load_json(FILE_AGENCIES_METADATA, raw_dir)  # agencies metadata

    # Data cleaning #
    
    # filter out duplicates
    df = df.drop_duplicates(subset="document_number", keep="first")
    
    # format dates; create column for year
    df.loc[:, "date"] = column_to_date(df, column="publication_date")
    df.loc[:, "year"] = df["date"].apply(lambda x: x.year)
    
    # clean president identifier
    df = clean_president_column(df)
    
    # clean up agencies column from API
    if "agencies_id_unique" in df.columns:
        pass
    else:
        df = clean_agencies_column(df, metadata=agencies_metadata)
    
    # clean agency info for export
    df.loc[:, "agency_names"] = df["agency_names"].apply(lambda x: "; ".join(x))
    cols = ["agencies_slug_uq", "agencies_id_uq", "agencies_acronym_uq", "agency_slugs"]
    for c in cols:
        df[c] = df[c].apply(lambda x: "; ".join(str(i) for i in x))

    # Save processed data
    save_csv(df, FILE_ALL_DATA_PROCESSED, processed_dir)


if __name__ == "__main__":
    retrieve_documents(YEARS_RANGE)
    process_documents()

