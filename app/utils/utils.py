from pandas import read_csv

def provide_dataframe(file_url: str):
    # read any thing and provide proper dataframe instance
    # link : str, validate as proper url
    # use link from file present in mande Studio
    # dataframe : dataframe
    # csv file path : str
    df = read_csv(file_url, na_values="NA")
    return df

