"""
Mark Febrizio
Last revised: 2023-01-30
"""

# --------------------------------------------------
# Initialize
import json
from pathlib import Path

from modules.federal_register_api import query_endpoint_documents

p = Path(__file__)
data_dir = p.parents[1].joinpath("data", "raw")
if data_dir.exists():
    pass
else:
    try:
        data_dir.mkdir(parents=True)
    except:
        print("Cannot create data directory.")

# --------------------------------------------------
# retrieve data from API
years = list(range(1994,2023))
documents = query_endpoint_documents(years)

# --------------------------------------------------
# export json file
file_path = data_dir / fr"documents_endpoint_{years[0]}_{years[-1]}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=4)
print("Exported as JSON!")

