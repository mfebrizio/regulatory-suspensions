# import dependencies
import json
from pathlib import Path
from pandas import DataFrame, read_csv


# -------------------------------------
# Functions for loading and saving data


def load_csv(file_name: str, 
             dir_path: Path = Path.cwd(), 
             add_nans = ["."]):
    """Load csv file using `open()` context manager.

    Args:
        file_name (str): Name of file to load.
        dir_path (Path, optional): Path to the directory. Defaults to Path.cwd().
        add_nans (list, optional): _description_. Defaults to ["."].

    Returns:
        DataFrame: Pandas DataFrame object containing the data.
    """    
    file_path = dir_path / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        df = read_csv(f, index_col=False, na_values=add_nans)
    return df


def load_json(file_name: str, 
              dir_path: Path = Path.cwd(),
              as_dataframe = True, 
              has_metadata = True, 
              data_key = "results"
              ):
    """Load json file using `open()` context manager.

    Args:
        file_name (str): Name of file to load.
        dir_path (Path, optional): Path to the directory. Defaults to Path.cwd().
        as_dataframe (bool, optional): Returns object as pandas DataFrame. Defaults to True.
        has_metadata (bool, optional): JSON object includes metadata (triggers use of data_key). Defaults to True.
        data_key (str, optional): Dict key where data is contained within JSON ojbect. Defaults to "results".

    Returns:
        dataset: A pandas DataFrame (default) or dict-like object containing the data.
    """
    file_path = dir_path / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # check if JSON object has metadata
    if has_metadata:
        data = data[data_key]
        
    # determine what format to return data
    if as_dataframe:
        df = DataFrame(data)
        return df
    else:
        return data


def save_csv(df: DataFrame, 
             file_name: str, 
             dir_path: Path = Path.cwd()
             ):
    """Export csv file using `open()` context manager.

    Args:
        df (DataFrame): Pandas DataFrame to save.
        file_name (str): Name of file.
        dir_path (Path, optional): Path to the directory. Defaults to Path.cwd().
    
    Returns:
        None
    """
    file_path = dir_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False, lineterminator=r"\n")


def save_json(obj, 
              file_name: str, 
              dir_path: Path = Path.cwd()
              ):
    """Export json file using `open()` context manager.

    Args:
        obj (dict-like): JSON-compatible object to save.
        file_name (str): Name of file.
        dir_path (Path, optional): Path to the directory. Defaults to Path.cwd().
    
    Returns:
        None
    """
    file_path = dir_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4)

