# import dependencies
from datetime import date
import json
from pathlib import Path
import requests


class AgencyMetadata:
    """Class for storing and transforming agency metadata from Federal Register API.
    
    Accepts a JSON object of structure iterable[dict].
    
    Methods:
        transform: Transform metadata from Federal Register API.
        save_json: Save transformed metadata.
    """    
    def __init__(self, data):
        self.data = data
        self.transformed_data = {}
    
    def transform(self):
        """Transform self.data from original format of iterable[dict] to dict[dict].
        
        Args:
            self
        
        Returns:
            None
        """        
        if self.transformed_data != {}:
            print("Metadata already transformed! Access it with self.transformed_data.")
        else:
            agency_dict = {}
            for i in self.data:
                if type(i) == dict:  # check if type is dict
                    slug = str(i.get("slug", "none"))
                    agency_dict.update({slug: i})                    
                else:  # cannot use this method on non-dict structures
                    continue
            while "none" in agency_dict:
                agency_dict.pop("none")
            # return transformed data as a dictionary
            self.transformed_data = agency_dict
    
    def save_json(self, 
                  data_dir: Path = Path(__file__).parents[1].joinpath("data", "raw"), 
                  file_name: str = r"agencies_endpoint_metadata.json"):
        """Save metadata on agencies from Federal Register API.

        Args:
            self
            data_dir (Path, optional): Path for saving JSON. Defaults to Path(__file__).parents[1].joinpath("data", "raw").
            file_name (str, optional): File name to use when saving. Defaults to r"agencies_endpoint_metadata.json".
        
        Returns:
            None
        """
        # create dictionary of data with retrieval date
        dict_metadata = {"source": "Federal Register API, https://www.federalregister.gov/reader-aids/developer-resources/rest-api",
                        "endpoint": r"https://www.federalregister.gov/api/v1/agencies.json",
                        "date_retrieved": str(date.today()),
                        "count": len(self.transformed_data), 
                        "results": self.transformed_data
                        }
        # export json file
        file_path = data_dir / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(dict_metadata, f, indent=4)


def query_endpoint_agencies(endpoint_url:str = r"https://www.federalregister.gov/api/v1/agencies.json"):
    """Queries the GET agencies endpoint of the Federal Register API.
    Retrieve agencies metadata. After defining endpoint url, no parameters are needed.

    Args:
        endpoint_url (str, optional): Endpoint for retrieving agencies metadata. Defaults to r"https://www.federalregister.gov/api/v1/agencies.json".

    Raises:
        Exception: Response status code if the request fails.

    Returns:
        list[dict]: response object in JSON format
    """
    # request documents; raise error if it fails
    agencies_response = requests.get(endpoint_url)
    if agencies_response.status_code != 200:
        raise Exception(f"API request failed. Status code: {agencies_response.status_code}")
    
    # return response as json
    return agencies_response.json()


def query_endpoint_documents(yearsList: list = [], 
                             doctypeList: list = ["RULE", "PRORULE", "NOTICE"], 
                             endpoint_url: str = r"https://www.federalregister.gov/api/v1/documents.json?"):
    """Queries the GET documents.{format} endpoint of the Federal Register API.

    Args:
        endpoint_url (str, optional): Endpoint for retrieving documents. Defaults to r"https://www.federalregister.gov/api/v1/documents.json?".

    Returns:
        dict: JSON object with metadata and retrieved documents.
    """    
    # --------------------------------------------------
    # define parameters
    res_per_page = 1000
    page_offset = 0  # both 0 and 1 return first page
    order = "oldest"
    fieldsList = ["publication_date", "president", "agencies", "agency_names", 
                  "document_number", "citation", "title", 
                  "type", "action", "dates", "abstract", 
                  "json_url", "correction_of", "corrections"
                  ]

    # dictionary of parameters
    dict_params = {"per_page": res_per_page,
                   "page": page_offset,
                   "order": order, 
                   "fields[]": fieldsList, 
                   "conditions[publication_date][year]": "", 
                   "conditions[type][]": doctypeList
                   }

    # --------------------------------------------------
    # retrieve data from Federal Register API
    # create objects
    dctsResults_all = []
    dctsCount_all = 0

    # for loop to pull data for each publication year
    for year in yearsList:
        print(f"\n***** Retrieving results for midnight period = {year} *****")

        dctsResults = []
        dctsCount = 0
        
        # update parameters for year
        dict_params.update({"conditions[publication_date][year]": year})

        # get documents
        dcts_response = requests.get(endpoint_url, params=dict_params)
        print(dcts_response.status_code,
                dcts_response.headers["date"],
                dcts_response.url, sep="\n")  # print request URL
        
        if dcts_response.json()["count"] != 0:
            
            # set variables
            dctsCount += dcts_response.json()["count"]
            
            try:  # for days with multiple pages of results
                dctsPages = dcts_response.json()["total_pages"]  # number of pages to retrieve all results
                
                # for loop for grabbing results from each page
                for page in range(1, dctsPages + 1):
                    dict_params.update({"page": page})
                    dcts_response = requests.get(endpoint_url, params=dict_params)
                    results_this_page = dcts_response.json()["results"]
                    dctsResults.extend(results_this_page)
                    print(f"Number of results retrieved = {len(dctsResults)}")
            
            except:  # when only one page of results
                results_this_page = dcts_response.json()["results"]
                dctsResults.extend(results_this_page)
                print(f"Number of results retrieved = {len(dctsResults)}")

        # create dictionary for year to export as json
        if len(dctsResults) == dctsCount:
            pass

        else:
            print(f"Counts do not align for {year}: {len(dctsResults)}  =/= {dctsCount}")

        # extend list of cumulative results and counts
        dctsResults_all.extend(dctsResults)
        dctsCount_all += dctsCount

    # create dictionary of data with retrieval date
    dctsRules = {"source": "Federal Register API, https://www.federalregister.gov/reader-aids/developer-resources/rest-api",
                 "endpoint": endpoint_url,
                 "date_retrieved": f"{date.today()}",
                 "count": dctsCount_all,
                 "results": dctsResults_all
                }
    # return output if count (metadata) matches length of results (calculation)
    if dctsRules["count"] == len(dctsRules["results"]):
        print("\nDictionary with retrieval date created!")
        return dctsRules
    else:
        print("\nError creating dictionary...")


# only query agencies endpoint when run as script; save that output 
if __name__ == "__main__":
    agencies_response = query_endpoint_agencies()
    agencies_metadata = AgencyMetadata(agencies_response)
    agencies_metadata.transform()
    agencies_metadata.save_json()
else:
    pass

