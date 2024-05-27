-- models/economic_processed.sql

{{ config(materialized='table') }}

with clean_employment as (
    select
        munic_name,
        measure,
        value,
        to_date(substring(trim_year, 1, 4), 'YYYY') as year,
        'Construcción' as category
    from public.employment_building
    where measure = 'Dato' and trim_year between '2017 Primer trimestre' and '2021 Cuarto trimestre'

    union all

    select
        munic_name,
        measure,
        value,
        to_date(substring(trim_year, 1, 4), 'YYYY') as year,
        'Comercio' as category
    from public.employment_commerce
    where measure = 'Dato' and trim_year between '2017 Primer trimestre' and '2021 Cuarto trimestre'

    union all

    select
        munic_name,
        measure,
        value,
        to_date(substring(trim_year, 1, 4), 'YYYY') as year,
        'Hostelería' as category
    from public.employment_hostelry
    where measure = 'Dato' and trim_year between '2017 Primer trimestre' and '2021 Cuarto trimestre'

    union all

    select
        munic_name,
        measure,
        value,
        to_date(substring(trim_year, 1, 4), 'YYYY') as year,
        'Servicios' as category
    from public.employment_services
    where measure = 'Dato' and trim_year between '2017 Primer trimestre' and '2021 Cuarto trimestre'

    union all

    select
        munic_name,
        measure,
        value,
        to_date(substring(trim_year, 1, 4), 'YYYY') as year,
        'Total' as category
    from public.employment
    where measure = 'Dato' and trim_year between '2017 Primer trimestre' and '2021 Cuarto trimestre'
),

clean_unemployment as (
    select
        munic_name,
        measure,
        value,
        to_date(substring(month_year, 1, 4), 'YYYY') as year
    from public.unemployment
    where measure = 'Dato' and month_year between '2017 Enero' and '2021 Diciembre'
),

combined_employment as (
    select
        munic_name,
        year,
        sum(case when category = 'Total' then value else 0 end) as employment_total,
        sum(case when category = 'Construcción' then value else 0 end) as employment_building,
        sum(case when category = 'Comercio' then value else 0 end) as employment_commerce,
        sum(case when category = 'Hostelería' then value else 0 end) as employment_hostelry,
        sum(case when category = 'Servicios' then value else 0 end) as employment_services
    from clean_employment
    group by munic_name, year
),

combined_unemployment as (
    select
        munic_name,
        year,
        sum(value) as unemployment_total
    from clean_unemployment
    group by munic_name, year
),

combined_income as (
    select
        munic_name,
        to_date(year::text, 'YYYY') as year,
        sum(value) as income_per_household
    from public.income_per_household
    where year between 2017 and 2021
    group by munic_name, year
),

combined_personal_income as (
    select
        munic_name,
        to_date(year::text, 'YYYY') as year,
        sum(value) as income_per_person
    from public.income_per_person
    where year between 2017 and 2021
    group by munic_name, year
),

economic_data as (
    select
        e.munic_name,
        e.year,
        e.employment_total,
        e.employment_building,
        e.employment_commerce,
        e.employment_hostelry,
        e.employment_services,
        u.unemployment_total,
        i.income_per_household,
        p.income_per_person,
        m.munic_cp
    from combined_employment e
    left join combined_unemployment u on e.munic_name = u.munic_name and e.year = u.year
    left join combined_income i on e.munic_name = i.munic_name and e.year = i.year
    left join combined_personal_income p on e.munic_name = p.munic_name and e.year = p.year
    join public.municipality_master m on e.munic_name = m.munic_name
)

select * from economic_data
order by munic_cp asc, year desc
