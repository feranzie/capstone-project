from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(log_prints=True, retries=3)
def extract_from_gcs(dataset_file:str) ->Path:
    """download data from gcs"""
    gcs_path=f"{dataset_file}.parquet"
    gcs_block= GcsBucket.load("capstone")
    print('found')
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")

@task()
def transform( path:Path) -> pd.DataFrame:
    """DAta cleaning example"""
    df=pd.read_parquet(path)
    df["HDI for year"].fillna(0, inplace=True)

    df.drop(["country-year" ], axis=1, inplace=True)
    df = df.rename(columns={'suicides/100k pop': 'suicides per 100k'})
    df = df.rename(columns={' gdp_for_year ($) ': 'gdp_for_year'})
    df = df.rename(columns={'gdp_per_capita ($)': 'gdp_per_capita'})
    print(f"pre :missing HDI for year:{df['HDI for year'].isna().sum()}")
    df.dropna(inplace=True)
    return df
@task()
def write_bq(df:pd.DataFrame) -> None:
    """write to big query"""
    gcp_credentials_block = GcpCredentials.load("capstonr")
    df.to_gbq(
        destination_table="suicide_data.capstone_suicide",
        project_id="capstone-420320",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="replace",
        )
    
@flow()
def etl_gcs_to_bq():
    """tHE MAIN etll function"""
 
    dataset_file="..\data\suicide-rates-overview-1985-to-2016"
     
    path=extract_from_gcs(dataset_file)
    df=transform(path)
    write_bq(df)
if __name__=="__main__":
    etl_gcs_to_bq() 



# df.drop(columns=['HDI for year',"country-year"], inplace=True)
    # df.dropna(inplace=True)