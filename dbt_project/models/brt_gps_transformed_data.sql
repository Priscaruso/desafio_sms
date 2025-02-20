-- sets configuration to generate a table using the queries below
{{ config(
    materialized='table',
    unique_key='id',
    ) }}

-- selects the id, the position and the speed from BRT GPS data generated in 'gps_brt' table
SELECT  codigo AS id,
        point(longitude,latitude) AS posicao,
        velocidade
FROM {{ source('brt_data', 'gps_brt') }} -- reference to table 'gps_brt' in source.yml file