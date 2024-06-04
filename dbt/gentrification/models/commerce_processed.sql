-- models/commerce_processed.sql

{{ config(materialized='table') }}

with pivoted_data as (
    select
        m.munic_cp,
        c.munic_name,
        to_date(c.year::text, 'YYYY') as year,
        max(case when c.category = 'Actividades inmobiliarias' then c.value else 0 end) as num_realestate,
        max(case when c.category = 'Hostelería' then c.value else 0 end) as num_hostelry,
        max(case when c.category = 'Actividades artísticas, recreativas y de entretenimiento' then c.value else 0 end) as num_entertainment,
        max(case when c.category = 'Construcción' then c.value else 0 end) as num_building
    from (
        select
            munic_name,
            year,
            category,
            value
        from public.commerce_building
        where year between 2017 and 2021

        union all

        select
            munic_name,
            year,
            category,
            value
        from public.commerce_entertainment
        where year between 2017 and 2021

        union all

        select
            munic_name,
            year,
            category,
            value
        from public.commerce_hostelry
        where year between 2017 and 2021

        union all

        select
            munic_name,
            year,
            category,
            value
        from public.commerce_realestate
        where year between 2017 and 2021
    ) c
    join public.municipality_master m on c.munic_name = m.munic_name
    group by m.munic_cp, c.munic_name, c.year
)

select * from pivoted_data
order by munic_cp asc, year desc
