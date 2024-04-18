# Suicide dataset analysis

## Data Engineering ZoomCamp 2024 Course Project 

1. [Preface](#preface)
2. [Technologies used](#technologies-used)
3. [Dataset description](#dataset-description)
4. [Data visualization: Dashboards](#data-visualization-dashboards)
5. [How to reproduce this Project](#how-to-reproduce-this-project)
  - [Requirements](#requirements)
  - [Step 1: Setup local Conda environment](#step-1-setup-local-conda-environment)
  - [Step 2: Setup GCP](#step-2-setup-gcp)
  - [Step 3: Setup terraform](#step-3-setup-terraform)
  - [Step 4: Kaggle setup](#step-4-kaggle-setup)
  - [Step 5: Prefect setup](#step-5-prefect-setup)
  - [Step 6: DBT setup](#step-6-dbt-setup)

## Preface

This repository contains the course project for the Data Engineering Zoomcamp (Cohort 2024) organized by the by DataTalksClub

Problem description: This project's aim is to draw insights on factors that influence suicide rates .
Dataset contains information of suicide rates of countries from 1985 to 2015, age, sex, number of suicides, gdp per year, gdp per capita...

- Is there a relationship between rate of suicide rates and economic factors?
- Which countries have the highest suicide rate?
- What age group has the highest suicide rate?

## Technologies used:
&emsp;Infrastructure as Code: [Terraform](https://www.terraform.io)      
&emsp;Workflow Orchestration: [Prefect](https://www.prefect.io)   
&emsp;Data Transformation: [dbt](https://www.getdbt.com)  
&emsp;Data Lake: [Google Cloud Storage](https://cloud.google.com/storage)     
&emsp;Data Warehouse: [Google BigQuery](https://cloud.google.com/bigquery)    
&emsp;Visualisation: [Looker Studio](http://lookerstudio.google.com/)  


## Dataset description

Dataset of countries with their number of suicides per year:
- economic factors per year like GDP per capita(economic output of a nation per person), Human development index for the year
- gender information,age...

It includes 12 variables for each country between the years 1985-2015



- Dataset on GCP is partioned by country and year.

More information about this dataset is available on [Kaggle](https://www.kaggle.com/datasets/russellyates88/suicide-rates-overview-1985-to-2016)

### dbt model dag diagram

![dag.jpg](https://github.com/feranzie/suicide-data-insights/blob/master/images/dag.jpg)

## Data visualization: Dashboards

The dashboard is live at [this link](https://lookerstudio.google.com/reporting/6e1e04cf-e8f2-443e-b817-85fb7ba02974)
- Below are a couple of insights drawn from the analysis:
- The gender based suicide distribution shows that men commmit more suicide than women
- The suicide age distrobution shows thet people in their midlife between ages (35-54) comit the most suicide
- The relationship between gdp per capita and suicide rates shows a direct correlation between gdp per capita and suiciide rates
- The Amount of suicides per country plot shows that russua has the highest suicide rate



## How to reproduce this Project

### Requirements

&emsp;1. [Anaconda](https://www.anaconda.com/)<br>
&emsp;2. [Git](https://git-scm.com/)<br>
&emsp;3. [Kaggle](https://www.kaggle.com/) free account<br>
&emsp;4. [Google Cloud Platform]() account<br>

### Step 1: Setup local Conda environment

1. Create conda environment and install pip
```bash
$ conda create --name <env-name>
$ conda activate <env-name>
$ conda install pip
```
2. Clone the project and change to project's directory
```bash
$ git clone https://github.com/feranzie/suicide-data-insights.git
$ cd suicide-data-insights
```
3. Install rest of requirements
```bash
$ pip install -r requirements.txt
```
### Step 2: Setup GCP

1. Create new project on [Google Cloud Platform](https://console.cloud.google.com/projectcreate) and **remember the project's name**, it will be needed later. 


- Edit ```environment``` file and set *PROJECT_ID* parameter with the project's name.

```bash
$ grep ^PROJECT_ID environment
PROJECT_ID="<project name>"
```

2. Create a Service Account:
    - Go to **IAM & Admin > Service accounts > Create service account** and create it

- Provide a service account name and grant the roles: **Viewer**, **BigQuery Admin**, **Storage Admin**, **Storage Object Admin**

- Create and download the Service Account key file (json format)

3. Edit ```environment``` file and set *GOOGLE_APPLICATION_CREDENTIALS* to point to location where downloaded json file exists.

```bash
$ grep ^GOOGLE_APP environment
GOOGLE_APPLICATION_CREDENTIALS="<path to service account on local system>"
```
4. Source the ```environment``` file.
```bash
$ . ./environment
```

### Step 3: Setup terraform

1. Install [Terraform](https://www.terraform.io) and place binary in path location
2. Modify terraform/variables.tf file and set GCP project ID. 

```bash
variable "project" {
  description = "Your GCP Project ID"
  default = "<Your GCP Project ID>"
  type= string
}

```
3. change directory to terraform and init it

```bash
$ cd terraform
$ terraform init
```

4. set up bucket and BigQuery structure

```bash
$ terraform plan
$ terraform apply
```

### Step 4: Kaggle setup

On [Kaggle](https://www.kaggle.com/) go to [Account Settings](https://www.kaggle.com/settings/account) and create new API token.
Put downloaded kaggle.json file in kaggle local computer path e.g C:\Users\DELL\.kaggle

### Step 5: Prefect setup

1. Run Prefect server on second terminal window

```bash
$ conda activate <env-name>
$ prefect orion start
```

2. Open [Prefect dashboard](http://127.0.0.1:4200) and go to Blocks section

- Add new Block named "GCP Credentials" and fill it with name (same as in *GCP_CREDENTIALS* parameter in ```environment``` file) and paste content of GCP Service Account key json file on Service Account Info section.


- go back to Blocks and add another one - GCS Bucket. Fill the Block Name with *GCP_BUCKET* parameter in ```environment``` file, set name of bucket and set Gcp Credentials to Block created above.


3. Go to prefect directory and run both python files. All flows should be completed.

```bash
$ cd prefect
$ python etl_web_to_gcs.py
$ python etl_gcs_to_bq.py
```

### Step 6: DBT setup

1. Go to dbt directory and init it as below

```
$ dbt init
 fill the values prompted
```

2. Check if all settings are working fine.

```
$ dbt debug
```


3. Install dependencies

```
$ dbt deps
Update your versions in packages.yml, then run dbt deps
```

4. Modify ```models/staging/schema.yml``` file and set databse setting to match your *GCP project ID*

```bash
$ grep database models/staging/schema.yml
    database: <name of your database>
```

5. Run dbt, views should be created successfully

```bash
$ dbt run
```

6. If you have an error that dataset is not found in location EU (404 Not found) please change the location parameter in profiles.yml to data location where BigQuery dataset is:























visualization: https://lookerstudio.google.com/reporting/6e1e04cf-e8f2-443e-b817-85fb7ba02974
