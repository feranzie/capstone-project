
import os
from datetime import timedelta
from pathlib import Path
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from prefect_gcp.cloud_storage import GcsBucket
from prefect import flow, task

DATA_DIR = '../data'
DATASET_NAME = 'suicide-rates-overview-1985-to-2016'
local_name='master.csv'
@task(name="Fetch data from Kaggle", retries=3, cache_expiration=timedelta(days=1), log_prints=True)
def fetch() -> None:
    """
    # go to https://www.kaggle.com/settings/account
    # API -> Create New Token
    # copy kaggle.json to .kaggle path in disk, C:/users/DELL/.kaggle in my case
     """
    api = KaggleApi()
    api.authenticate()
    print('here')
    api.dataset_download_files(
        f'russellyates88/{DATASET_NAME}',
        path=DATA_DIR, unzip=True)
    df=pd.read_csv(f"../data/{local_name}")
    return df

    

@task(log_prints=True)
def clean(df= pd.DataFrame) -> pd.DataFrame:
    "fix dtype issues"
    df[ ' gdp_for_year ($) '] = df[ ' gdp_for_year ($) '].str.replace(',', '').astype(float)
    # df['country'] = df['country'].astype(str)
    # df['sex'] = df['sex'].astype(str)
    # df['generation'] = df['generation'].astype(str)
    # df.drop(columns=['HDI for year',"country-year"], inplace=True)
    # df.dropna(inplace=True)
    print(df.head(2))
    print(f"rows: {len(df)}")
    return df

@task()
def write_local(df: pd.DataFrame, DATASET_NAME:str)-> Path:
    """write dataframe out locally a parquet"""
    path=Path(f"../data/{DATASET_NAME}.parquet")
    df.to_parquet(path,compression="gzip")
    return path

@task()
def write_gcs(path:Path)-> None:
    """write to gcs"""
    print("gooogle buckettt")
    gcs_block=GcsBucket.load("capstone")
    gcs_block.upload_from_path(from_path=f"{path}", to_path=path)
    return
    

@flow()
def etl_web_gcs() -> None:
    """tHE MAIN etll function"""
    df=fetch()
    df_clean=clean(df)
    path=write_local(df_clean,DATASET_NAME)
    write_gcs(path)

if __name__ == '__main__':
    etl_web_gcs()




