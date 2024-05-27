-- models/security_processed.sql

{{ config(materialized='table') }}

with security_data as (
    select
        munic_name,
        to_date(year::text, 'YYYY') as year,
        value as number_crimes
    from public.security
    where to_date(year::text, 'YYYY') between '2017-01-01' and '2021-12-31'
),

average_crimes as (
    select
        avg(number_crimes)::int as avg_crimes
    from security_data
),

years as (
    select generate_series('2017-01-01'::date, '2021-12-31'::date, '1 year')::date as year
),

all_municipalities as (
    select
        m.munic_cp,
        m.munic_name,
        y.year,
        coalesce(s.number_crimes::int, a.avg_crimes) as number_crimes
    from years y
    cross join public.municipality_master m
    left join security_data s on m.munic_name = s.munic_name and y.year = s.year
    cross join average_crimes a
)

select * from all_municipalities
order by munic_cp asc, year desc
