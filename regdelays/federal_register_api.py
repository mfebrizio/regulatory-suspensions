# standard library
import json
from datetime import date
from pathlib import Path

# third party libraries
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
            data_dir (Path, optional): Path for saving JSON. Defaults to Path(__file__).parents[1].joinpath("data", "raw").
            file_name (str, optional): File name to use when saving. Defaults to r"agencies_endpoint_metadata.json".
        
        Returns:
            None
        """
        # create dictionary of data with retrieval date
        dict_metadata = {"source": "Federal Register API, https://www.federalregister.gov/reader-aids/developer-resources/rest-api",
                         "endpoint": r"https://www.federalregister.gov/api/v1/agencies.json",
                         "date_retrieved": f"{date.today()}",
                         "count": len(self.transformed_data), 
                         "results": self.transformed_data
                        }
        # export json file
        file_path = data_dir / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(dict_metadata, f, indent=4)


def query_endpoint_agencies(endpoint_url: str = r"https://www.federalregister.gov/api/v1/agencies.json"):
    """Queries the GET agencies endpoint of the Federal Register API.
    Retrieve agencies metadata. After defining endpoint url, no parameters are needed.

    Args:
        endpoint_url (str, optional): Endpoint for retrieving agencies metadata. Defaults to r"https://www.federalregister.gov/api/v1/agencies.json".

    Raises:
        HTTPError: via requests package

    Returns:
        list[dict]: response object in JSON format
    """
    # request documents; raise error if it fails
    agencies_response = requests.get(endpoint_url)
    if agencies_response.status_code != 200:
        print(agencies_response.reason)
        agencies_response.raise_for_status()
    
    # return response as json
    return agencies_response.json()


def get_documents(endpoint_url: str, dict_params: dict):
    """Send a GET request to retrieve documents from API endpoint.

    Args:
        endpoint_url (str): Retrieve documents from this endpoint.
        dict_params (dict): Parameters to send with the request.

    Returns:
        tuple[list, int]: Tuple of retrieved documents, count of documents.
    """
    dctsResults = []
    dctsCount = 0
    dcts_response = requests.get(endpoint_url, params=dict_params)
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
                #print(f"Number of results retrieved = {len(dctsResults)}")
        
        except:  # when only one page of results
            results_this_page = dcts_response.json()["results"]
            dctsResults.extend(results_this_page)
            #print(f"Number of results retrieved = {len(dctsResults)}")
        
    return dctsResults, dctsCount


def query_endpoint_documents(yearsList: list,  
                             doctypeList: list = ["RULE", "PRORULE", "NOTICE"], 
                             fieldsList: list = ["publication_date", "president", 
                                                 "agencies", "agency_names", 
                                                 "document_number", "citation", 
                                                 "title", "type", 
                                                 "action", "dates", 
                                                 "abstract", "json_url", 
                                                 "correction_of", "corrections"], 
                             endpoint_url: str = r"https://www.federalregister.gov/api/v1/documents.json?", 
                             increment_by_quarter: bool = True
                             ):
    """Queries the GET documents.{format} endpoint of the Federal Register API.

    Args:
        yearsList (list): Years when documents were published. API only dates back to 1994.
        doctypeList (list, optional): Document types to return in request. Defaults to ["RULE", "PRORULE", "NOTICE"].
        fieldsList (list, optional): Fields to return for each document. Defaults to ["publication_date", "president", "agencies", "agency_names", "document_number", "citation", "title", "type", "action", "dates", "abstract", "json_url", "correction_of", "corrections"].
        endpoint_url (str, optional): Endpoint for retrieving documents. Defaults to r"https://www.federalregister.gov/api/v1/documents.json?".

    Returns:
        dict: JSON object with metadata and retrieved documents.
    """    
    # --------------------------------------------------
    # define parameters
    res_per_page = 1000
    page_offset = 0  # both 0 and 1 return first page
    order = "oldest"

    # dictionary of parameters
    dict_params = {"per_page": res_per_page,
                   "page": page_offset,
                   "order": order, 
                   "fields[]": fieldsList, 
                   "conditions[type][]": doctypeList
                   }

    # --------------------------------------------------
    # retrieve data from Federal Register API
    # create objects
    dctsResults_all = []
    dctsCount_all = 0
    
    # for loop to pull data for each publication year
    for year in yearsList:
        print(f"\n***** Retrieving results for time period = {year} *****")

        dctsResults = []
        dctsCount = 0
        
        # update date parameters
        if increment_by_quarter:
            # format: YYYY-MM-DD
            quarter_tuples = [("01-01", "03-31"), ("04-01", "06-30"), 
                              ("07-01", "09-30"), ("10-01", "12-31")]
            
            for quarter in quarter_tuples:            
                dctsResults_qrt = []
                dctsCount_qrt = 0
                # update parameters by quarter
                dict_params.update({"conditions[publication_date][gte]": f"{year}-{quarter[0]}", 
                                    "conditions[publication_date][lte]": f"{year}-{quarter[1]}"}
                                   )
                # get documents
                dctsResults_qrt, dctsCount_qrt = get_documents(endpoint_url, dict_params)
                dctsResults.extend(dctsResults_qrt)
                dctsCount += dctsCount_qrt
        else:
            # update parameters by year
            dict_params.update({"conditions[publication_date][year]": year})
            
            # get documents
            dctsResults, dctsCount = get_documents(endpoint_url, dict_params)

        # print progress
        print(f"Number of results retrieved = {len(dctsResults)}")
        
        # raise error if documents fitting criteria are not retrieved
        if len(dctsResults) != dctsCount:
            raise Exception(f"Counts do not align for {year}: {len(dctsResults)} =/= {dctsCount}")

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

