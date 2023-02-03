# import dependencies
from pandas import DataFrame


def clean_president_column(df_input: DataFrame, 
                            column: str = "president"):
    """Clean column containing president metadata for Federal Register API data.

    Args:
        df_input (DataFrame): Input dataframe.
        column (str, optional): Column containing president metadata. Defaults to "president".

    Returns:
        DataFrame: Copy of df_input with new column, "president_id".
    """    
    # create deep copy of input dataframe
    df = df_input.copy(deep=True)
    
    # handle missing values
    bool_mi = df["president"].isna()
    df.loc[bool_mi, "president"] = df["president"].interpolate('pad').loc[bool_mi]
    
    # extract president identifier
    df["president_id"] = df.apply(lambda x: x[column].get("identifier"), axis=1)
    president_list = list(set(df["president_id"].values.tolist()))
    print(", ".join(president_list))

    # return output df with new columns
    return df

