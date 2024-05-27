-- models/locations_processed.sql

{{ config(materialized='table') }}

with date_ranges as (
    select
        nombre,
        actividad_tipo,
        municipio_codigo,
        municipio_nombre,
        longitud,
        latitud,
        generate_series(
            date_trunc('year', to_date(fecha_creacion, 'YYYY-MM-DD')),
            date_trunc('year', to_date(fecha_actualizacion, 'YYYY-MM-DD')),
            interval '1 year'
        ) as year
    from (
        select nombre, actividad_tipo, municipio_codigo, municipio_nombre, longitud, latitud, fecha_creacion, fecha_actualizacion from public.locations_commerce
        union all
        select nombre, actividad_tipo, municipio_codigo, municipio_nombre, longitud, latitud, fecha_creacion, fecha_actualizacion from public.locations_hostelry
        union all
        select nombre, actividad_tipo, municipio_codigo, municipio_nombre, longitud, latitud, fecha_creacion, fecha_actualizacion from public.locations_sport_leasure
        union all
        select nombre, actividad_tipo, municipio_codigo, municipio_nombre, longitud, latitud, fecha_creacion, fecha_actualizacion from public.locations_tourism_establishments
    ) as combined_locations
)

select
    nombre,
    actividad_tipo,
    municipio_codigo,
    municipio_nombre,
    longitud,
    latitud,
    year::date as year
from date_ranges
order by nombre desc, municipio_codigo asc
