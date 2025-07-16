{{
  config(
    materialized='incremental',
    unique_key='weather_data_id'
  )
}}

/*
This model builds upon the stg_weather_data model.
Its primary purpose is to cast data types to their most appropriate
format for downstream analysis and to perform final clean-up.

This model is configured as incremental, so on subsequent runs, dbt will only
process new records based on the loaded_at timestamp.
*/

with staged_data as (

    -- Selects from the previous staging model using the ref() function.
    -- This creates a dependency between this model and stg_weather_data.
    select * from {{ ref('stg_weather_data') }}

    -- This is the incremental logic block.
    {% if is_incremental() %}

      -- The is_incremental() macro returns 'true' if this is not the first run.
      -- The {{ this }} variable refers to the target table itself (stg_weather_data_final).
      -- This WHERE clause tells dbt to only fetch records from the source
      -- that are newer than the latest record already in the target table.
      where loaded_at > (select max(loaded_at) from {{ this }})

    {% endif %}

),

casted_data as (
    
    select
        weather_data_id,
        city,
        cast(temperature as integer) as temperature_celsius,
        weather_descriptions,
        cast(wind_speed as integer) as wind_speed_kph,
        observation_time,
        cast(utc_offset as numeric) as utc_offset,
        loaded_at

    from staged_data

)

select * from casted_data