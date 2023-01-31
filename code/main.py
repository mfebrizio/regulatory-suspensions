# Initialize
from pathlib import Path

from federal_register_api import query_endpoint_documents, query_endpoint_agencies, AgencyMetadata
from utils import save_json

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

# set variables
YEARS_OF_INTEREST = list(range(1994, 2023))


def retrieve_documents(years):
    """Retrieve and save documents from Federal Register API.
    """
    # retrieve data from API
    documents = query_endpoint_documents(years)

    # --------------------------------------------------
    # export json file
    file_name = fr"documents_endpoint_{years[0]}_{years[-1]}.json"
    save_json(documents, file_name, raw_dir)

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


if __name__ == "__main__":
    retrieve_documents(YEARS_OF_INTEREST)
    process_documents()

