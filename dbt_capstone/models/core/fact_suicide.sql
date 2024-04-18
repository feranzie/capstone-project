{{ config(materialized = "table") }}

select * from {{ ref('stg_suicide_data') }}