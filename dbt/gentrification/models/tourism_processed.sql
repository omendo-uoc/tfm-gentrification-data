-- models/tourism_processed.sql

{{ config(materialized='table') }}

with establishments_data as (
    select
        munic_name,
        to_date(year::text, 'YYYY') as year,
        value as open_establishments
    from public.tourism_establishments
    where to_date(year::text, 'YYYY') between '2017-01-01' and '2021-12-31'
),

spending_data as (
    select
        munic_name,
        to_date(year::text, 'YYYY') as year,
        value as tourism_spending
    from public.tourism_spending
    where to_date(year::text, 'YYYY') between '2017-01-01' and '2021-12-31'
),

average_establishments as (
    select
        avg(open_establishments)::int as avg_establishments
    from establishments_data
),

average_spending as (
    select
        avg(tourism_spending)::int as avg_spending
    from spending_data
),

years as (
    select generate_series('2017-01-01'::date, '2021-12-31'::date, '1 year')::date as year
),

combined_data as (
    select
        e.munic_name,
        e.year,
        e.open_establishments,
        s.tourism_spending
    from establishments_data e
    full join spending_data s on e.munic_name = s.munic_name and e.year = s.year
),

all_municipalities as (
    select
        m.munic_cp,
        m.munic_name,
        y.year,
        coalesce(c.open_establishments, a.avg_establishments) as open_establishments,
        coalesce(c.tourism_spending, b.avg_spending) as tourism_spending
    from years y
    cross join public.municipality_master m
    left join combined_data c on m.munic_name = c.munic_name and y.year = c.year
    cross join average_establishments a
    cross join average_spending b
)

select * from all_municipalities
order by munic_cp asc, year desc
