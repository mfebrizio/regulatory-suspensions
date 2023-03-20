# import dependencies
import random
import numpy as np
import pandas as pd


def simple_random_sample(df: pd.DataFrame, 
                         id_column: str, 
                         sample_size: int, 
                         seed = 42
                         ):
    """Draw a simple random sample (also called a probability sample) from a dataset, using a unique id.

    Args:
        df (pd.DataFrame): DataFrame of sampling frame.
        id_column (str): Column indicating unique id of data.
        sample_size (int): Number of units to include in sample.
        seed (int, optional): Seed for random module. Defaults to 42.

    Returns:
        tuple: sampled DataFrame, unsampled DataFrame.
    """
    # create a copy of dataframe
    dfCoding = df.copy(deep=True)
    id_list = dfCoding[id_column].values.tolist()
    print(f"Sampling frame: {len(id_list)}")

    # use random library to define sample
    random.seed(a=seed)
    sample_list = random.sample(id_list, sample_size)
    print(f"Sample size: {len(sample_list)}")
    print(f"Proportion: {round(len(sample_list)/len(id_list)*100, 2)}%")

    # filter out sampled Ids
    bool_sample = np.array([True if i in sample_list else False for i in id_list])
    dfSample = dfCoding.loc[bool_sample, :]
    dfUnsampled = dfCoding.loc[~bool_sample, :]
    
    # return tuple of dataframes
    return dfSample, dfUnsampled


def stratified_random_sample(df: pd.DataFrame, 
                             id_column: str, 
                             strata_column: str, 
                             sample_size: int, 
                             proportionate: bool = True, 
                             seed: int = 42
                             ):
    """Draw a stratified random sample (also called a probability sample) from a dataset, using a unique id and a column that separates the data into strata.
    Reference for proportionate vs. disproportionate methods: [Investopedia](https://www.investopedia.com/terms/stratified_random_sampling.asp).
    
    Args:
        df (pd.DataFrame): Input DataFrame for sampling.
        id_column (str): Column name for unique ids.
        strata_column (str): Column name for stratification.
        sample_size (int): Total number of samples to draw.
        proportionate (bool, optional): Determines whether sampling is proportionate to the strata. Defaults to True.
        seed (int, optional): Seed for initializing random number generator. Defaults to 42.

    Raises:
        TypeError: When parameter 'proportionate' does not receive type bool.
        Exception: When the sample per strata does not add up to total sample size requested.

    Returns:
        tuple: sampled DataFrame, unsampled DataFrame
    """
    # copy dataframe and create lists from parameters
    dfCoding = df.copy(deep=True)
    id_list = dfCoding[id_column].values.tolist()
    strata_list = list(set(dfCoding[strata_column].values.tolist()))  # use set function to get unique values
    print(f"Sampling frame: {len(id_list)}", 
          f"# strata ({strata_column}): {len(strata_list)}", sep="\n")
    
    # evaluate whether to draw proportionate stratified sample
    if proportionate == True:  # aggregate data and calculate proportion of each strata to population
        dfAgg = dfCoding.groupby(strata_column).agg({id_column: "count"}).reset_index()
        dfAgg.loc[:, "proportion"] = dfAgg[id_column] / len(id_list)
        dfAgg.loc[:, "sample"] = round(dfAgg["proportion"] * sample_size, 0)
        strata_list = dfAgg[strata_column].values.tolist()
        sample_per_strata = [int(i) for i in dfAgg["sample"].values]    
    elif proportionate == False:  # determine equally sized samples to draw for disproportionate sampling
        remainder = sample_size % len(strata_list)
        if remainder == 0:
            sample_per_strata = [sample_size / len(strata_list)] * len(strata_list)
        elif remainder != 0:  # handles instances with a remainder
            sample_per_strata = [sample_size // len(strata_list)] * len(strata_list)
            sample_per_strata[0] = sample_per_strata[0] + remainder  # first strata receives extra remainder values
    else:  # catches instances where 'proportionate' does not receive True/False value
        raise TypeError("Parameter 'proportionate' must be type bool.")
    
    # check if stratified sample matches sample_size
    if sum(sample_per_strata) != sample_size:
        raise Exception(f"Error defining sample sizes per strata: {sample_per_strata} does not sum to {sample_size}.")
    else:
        print(f"Drawing {sample_size} samples...")
    
    # draw samples
    random.seed(a=seed)  # set seed for random number generator
    sample_list = []
    for strata, sample in zip(strata_list, sample_per_strata):            
        bool_strata = np.array(dfCoding[strata_column] == strata)
        sample_strata = random.sample(dfCoding.loc[bool_strata, "documentId"].values.tolist(), sample)
        sample_list.extend(sample_strata)

    # filter out sampled ids
    bool_sample = np.array([True if i in sample_list else False for i in id_list])
    dfSample = dfCoding.loc[bool_sample, :]
    dfUnsampled = dfCoding.loc[~bool_sample, :]
    
    # return tuple of dataframes
    return dfSample, dfUnsampled


def random_gen_sort(df: pd.DataFrame, seed: int = 42, sort_data: bool = True):
    """Generates a column of random numbers and sorts the dataframe.

    Args:
        df (pd.DataFrame): Input dataframe.
        seed (int, optional): Seed for initializing random number generator. Defaults to 42.
        sort_data (bool, optional): Sort data based on random numbers. Defaults to True.

    Returns:
        pd.DataFrame: Copy of dataframe, sorted by random column.
    """    
    # set seet for RNG
    random.seed(a=seed)
    
    # generate a list of random numbers
    rand_list = [random.random() for i in range(len(df))]
    print(f"Random numbers generated: {len(rand_list)}")

    # add random var to copy of dataframe
    dfcopy = df.copy(deep=True)
    dfcopy.loc[:, "random"] = rand_list

    if sort_data:
        # sort dataframe by random variable
        dfcopy = dfcopy.sort_values("random", axis=0, ascending=True, ignore_index=False)
    
    # return sorted dataframe
    return dfcopy


def calculate_assignment_sizes(number_of_coders: int, 
                               sample_size: int, 
                               overlap_options: list
                               ):
    """Calculate the size of coder assignments for comparison with alternatives.

    Args:
        number_of_coders (int): Number of coders that will be assigned a coding set.
        sample_size (int): The total size of the coding sample.
        overlap_options (list): A list of options for the size of the reliability sample.

    Returns:
        dict: Potential coder assignment sizes for each overlap option. 
    """    
    assignment_sizes = {}
    for overlap in overlap_options:
        unique = sample_size - overlap
        split_unique = unique // number_of_coders
        remainder = unique % number_of_coders
        option = split_unique + overlap
        
        this_assignment = {"num_coders": number_of_coders, 
                           "percent_overlap": round(overlap / sample_size * 100, 2), 
                           "total_unique_comments": unique, 
                           "unique_split": split_unique, 
                           "coder_assignment_size": option, 
                           "remainder": remainder
                           }
        assignment_sizes[f"{overlap}"] = this_assignment
    
    return assignment_sizes


def create_coder_assignments(df_tuple: tuple, coders: list, sort_column: str = "random"):
    """Create coder assignments by combining coding data with reliability sample.

    Args:
        df_tuple (tuple): Tuple of input DataFrames, one with sampled data and another with unsampled data.
        coders (list): Ids of coders to receive coding assignments.
        sort_column (str, optional): Column name used to sort values. Defaults to "random".

    Raises:
        Exception: When function cannot differentiate between sample and non-sample data (e.g., input DataFrames are of the same length).

    Returns:
        list: List of DataFrames containing coder assignments. Example: [dfAssignment1, dfAssigment2, ..., dfAssignment_n]
    """
    # assumption: sampled data will be less than unsampled data
    if len(df_tuple[0]) < len(df_tuple[1]):  # tuple: (sampled data, unsampled data)
        # split unsampled dataframe for n coders
        # https://numpy.org/doc/stable/reference/generated/numpy.array_split.html
        print(f"Create {len(coders)} dataframes of length ~{len(df_tuple[1]) // len(coders)}")
        split_df = np.array_split(df_tuple[1], len(coders), axis=0)

        # append reliability sample to each split df
        assignments = []
        for df in split_df:
            assign = pd.concat([df, df_tuple[0]], axis=0, join='outer', verify_integrity=True)
            assign = assign.sort_values(sort_column, axis=0, ascending=True, ignore_index=False)
            assignments.append(assign)
        print(f"{len(assignments)} assignments created!")
        
    elif len(df_tuple[0]) > len(df_tuple[1]):  # tuple: (unsampled data, sampled data)
        # split unsampled dataframe for n coders
        # https://numpy.org/doc/stable/reference/generated/numpy.array_split.html
        print(f"Create {len(coders)} dataframes of length ~{len(df_tuple[0]) // len(coders)}")
        split_df = np.array_split(df_tuple[0], len(coders), axis=0)

        # append reliability sample to each split df
        assignments = []
        for df in split_df:
            assign = pd.concat([df, df_tuple[1]], axis=0, join='outer', verify_integrity=True)
            assign = assign.sort_values(sort_column, axis=0, ascending=True, ignore_index=False)
            assignments.append(assign)
        print(f"{len(assignments)} assignments created!")
        
    else:
        raise Exception("Cannot differentiate sampled data from unsampled data.")
    
    # check to make sure assignments don't overlap
    for i, n in enumerate(assignments):
        assignlist = n["documentId"].values.tolist()  # store list of documentIds for assignment i
        print(f"\nAssignment {i}")
        for a in assignments:  # for each assignment a, compare length of overlapping documents with assignment i
            print(len([d for d in assignlist if d in a['documentId'].values.tolist()]))
    
    # return coder assignments
    return assignments

