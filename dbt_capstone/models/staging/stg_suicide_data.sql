
{{ config(materialized='view') }}

with suicidedata as 
(
  select *,
    row_number() over(partition by country, year) as rn
  from {{ source('staging','capstone_suicide') }}
)


select
    -- identifiers
    {{ dbt_utils.surrogate_key(['country', 'year']) }} as id,
    cast(country as string) as country,
    cast(year as integer) as year,
    cast(sex as string) as sex,
    cast(age as string) as age,
    cast(suicides_no as integer) as suicides_no,
    cast(population as integer) as population,
    cast(suicides_per_100k as integer) as suicides_per_100k,
    cast(HDI_for_year as numeric) as HDI_for_year,
    cast(gdp_for_year as numeric) as gdp_for_year,
    cast(gdp_per_capita	 as integer) as gdp_per_capita,
    cast(generation as string) as generation

from suicidedata
where rn = 1


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}