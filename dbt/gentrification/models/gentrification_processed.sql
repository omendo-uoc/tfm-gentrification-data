-- models/gentrification_processed.sql

{{ config(materialized='table') }}

with demography as (
    select
        munic_cp,
        munic_name,
        year,
        population_total::int,
        births::int,
        deaths::int,
        foreigns::int,
        migrations::int,
        mean_age::numeric
    from {{ ref('population_processed') }}
),

commerce as (
    select
        munic_cp,
        munic_name,
        year,
        num_realestate::int,
        num_hostelry::int,
        num_entertainment::int,
        num_building::int
    from {{ ref('commerce_processed') }}
),

housing as (
    select
        munic_cp,
        munic_name,
        year,
        sale_price_m2::numeric,
        rent_price_m2::numeric
    from {{ ref('housing_processed') }}
),

economic as (
    select
        munic_cp,
        munic_name,
        year,
        employment_total::int,
        employment_building::int,
        employment_commerce::int,
        employment_hostelry::int,
        employment_services::int,
        unemployment_total::int,
        income_per_household::numeric,
        income_per_person::numeric
    from {{ ref('economy_processed') }}
),

locations as (
    select
        municipio_codigo as munic_cp,
        municipio_nombre as munic_name,
        year,
        nombre,
        actividad_tipo,
        longitud::numeric,
        latitud::numeric
    from {{ ref('locations_processed') }}
),

security as (
    select
        munic_cp,
        munic_name,
        year,
        number_crimes::int
    from {{ ref('security_processed') }}
),

tourism as (
    select
        munic_cp,
        munic_name,
        year,
        open_establishments::int,
        tourism_spending::numeric
    from {{ ref('tourism_processed') }}
),

all_municipalities as (
    select
        m.munic_cp,
        m.munic_name,
        y.year
    from public.municipality_master m
    cross join (
        select distinct year from demography
        union
        select distinct year from commerce
        union
        select distinct year from housing
        union
        select distinct year from economic
        union
        select distinct year from security
        union
        select distinct year from tourism
    ) y
)

select
    am.munic_cp,
    am.munic_name,
    am.year,
    coalesce(d.population_total, 0) as population_total,
    coalesce(d.births, 0) as births,
    coalesce(d.deaths, 0) as deaths,
    coalesce(d.foreigns, 0) as foreigns,
    coalesce(d.migrations, 0) as migrations,
    coalesce(d.mean_age, 0::numeric) as mean_age,
    coalesce(c.num_realestate, 0) as number_realestate,
    coalesce(c.num_hostelry, 0) as number_hostelry,
    coalesce(c.num_entertainment, 0) as number_entertainment,
    coalesce(c.num_building, 0) as number_building,
    coalesce(h.sale_price_m2, 0::numeric) as sale_price_m2,
    coalesce(h.rent_price_m2, 0::numeric) as rent_price_m2,
    coalesce(e.employment_total, 0) as employment_total,
    coalesce(e.employment_building, 0) as employment_building,
    coalesce(e.employment_commerce, 0) as employment_commerce,
    coalesce(e.employment_hostelry, 0) as employment_hostelry,
    coalesce(e.employment_services, 0) as employment_services,
    coalesce(e.unemployment_total, 0) as unemployment_total,
    coalesce(e.income_per_household, 0::numeric) as income_per_household,
    coalesce(e.income_per_person, 0::numeric) as income_per_person,
    coalesce(s.number_crimes, 0) as number_crimes,
    coalesce(t.open_establishments, 0) as open_establishments,
    coalesce(t.tourism_spending, 0::numeric) as tourism_spending
from all_municipalities am
left join demography d on am.munic_cp = d.munic_cp and am.year = d.year
left join commerce c on am.munic_cp = c.munic_cp and am.year = c.year
left join housing h on am.munic_cp = h.munic_cp and am.year = h.year
left join economic e on am.munic_cp = e.munic_cp and am.year = e.year
left join security s on am.munic_cp = s.munic_cp and am.year = s.year
left join tourism t on am.munic_cp = t.munic_cp and am.year = t.year
order by am.munic_cp asc, am.year desc
