-- models/population_processed.sql

{{ config(materialized='table') }}


with population_data as (
    select
        m.munic_cp,
        p.munic_name,
        p.year,
        p.population_total,
        b.births,
        d.deaths,
        f.foreigns,
        mig.migrations,
        ma.mean_age
    from (
        select
            munic_name,
            to_date(year::text, 'YYYY') as year,
            value as population_total
        from public.population
        where measure = 'Dato' and year between 2017 and 2021
    ) p
    join (
        select
            munic_name,
            to_date(year::text, 'YYYY') as year,
            value as births
        from public.population_births
        where measure = 'Dato' and year between 2017 and 2021
    ) b on p.munic_name = b.munic_name and p.year = b.year
    join (
        select
            munic_name,
            to_date(year::text, 'YYYY') as year,
            value as deaths
        from public.population_deaths
        where measure = 'Dato' and year between 2017 and 2021
    ) d on p.munic_name = d.munic_name and p.year = d.year
    join (
        select
            munic_name,
            to_date(year::text, 'YYYY') as year,
            value as foreigns
        from public.population_foreing
        where measure = 'Dato' and year between 2017 and 2021
    ) f on p.munic_name = f.munic_name and p.year = f.year
    join (
        select
            munic_name,
            to_date(year::text, 'YYYY') as year,
            value as migrations
        from public.population_migrations
        where measure = 'Dato' and year between 2017 and 2021
    ) mig on p.munic_name = mig.munic_name and p.year = mig.year
    join (
        select
            munic_name,
            to_date(year::text, 'YYYY') as year,
            value as mean_age
        from public.population_mean_age
        where measure = 'Dato' and year between 2017 and 2021
    ) ma on p.munic_name = ma.munic_name and p.year = ma.year
    join public.municipality_master m on p.munic_name = m.munic_name
)

select * from population_data
order by munic_cp asc, year desc