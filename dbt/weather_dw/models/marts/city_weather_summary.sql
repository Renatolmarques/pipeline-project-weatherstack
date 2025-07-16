/*
This model creates a final "mart" table summarizing key weather metrics per city.
It aggregates data from the final staging layer to provide insights ready for
analytics and visualization. This represents our Gold layer.
*/

with final_staging_data as (

    -- Reference our final staging model
    select * from {{ ref('stg_weather_data_final') }}

)

select
    -- Grouping by city
    city,

    -- Aggregate Functions to calculate metrics
    count(*) as number_of_readings,
    avg(temperature_celsius) as avg_temperature,
    max(wind_speed_kph) as max_wind_speed,
    min(observation_time) as first_observation,
    max(observation_time) as latest_observation

from final_staging_data

group by 1 -- Corresponds to the first column in the select statement (city)
order by city