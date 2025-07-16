/*
This model selects and renames columns from the raw weather data source.
It serves as the first basic cleaning step, creating a staging layer 
that is closer to the analytical needs.

Renaming columns to be more descriptive and consistent is a key goal
of this staging model.
*/

with source_data as (

    select
        -- Primary key from the source table
        id as weather_data_id,
        
        -- Location information
        city,
        utc_offset,
        
        -- Observation timestamp and metadata
        time as observation_time,
        inserted_at as loaded_at, -- Renaming to clarify this is a load timestamp

        -- Weather metrics
        temperature,
        weather_descriptions,
        wind_speed

    from {{ source('weatherstack_raw_data', 'raw_weather_data') }}

)

-- Final selection of all columns from the CTE above
select * from source_data