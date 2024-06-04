-- models/housing_processed.sql

{{ config(materialized='table') }}

with housing_data as (
    select
        m.munic_cp,
        h.munic_name,
        h.sale_price_m2::numeric,
        h.rent_price_m2::numeric,
        to_date(h.year::text, 'YYYY') as year
    from public.housing_prices h
    join public.municipality_master m on h.munic_name = m.munic_name
    where h.year between 2017 and 2021
)

select * from housing_data
order by munic_cp asc, year desc
