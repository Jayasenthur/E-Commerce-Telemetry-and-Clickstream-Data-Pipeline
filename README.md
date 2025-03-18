# From Clicks to Deliveries: Maximizing E-commerce Performance with Real-Time Data Integration

This project implements a real-time data pipeline for processing __Clickstream Data__ and __Truck Telemetry Data__ using AWS services (Kinesis, Lambda, DynamoDB, S3, Firehose) and Snowflake for data storage and analysis. The data is visualized using a __Streamlit UI__.

# Technologies Used
* __AWS Services:__
     * __Kinesis Data Streams__: For real-time data ingestion.
     * __Lambda Functions__: For data processing.
     * __DynamoDB__: For storing Clickstream data
     * __S3__ : For storing Truck Telemetry data.
     * __Firehose__: For loading data from Kinesis to S3.
     * __API Gateway__: For exposing the Truck Telemetry API.
* __Snowflake__: For data warehousing and analysis.
* __Streamlit__: For data visualization.
* __Python__: For scripting and data generation.

# Problem Statement
As an e-commerce company, our success hinges on seamlessly integrating our online platform with efficient logistics management to ensure optimal customer satisfaction and operational efficiency. To achieve this synergy, we aim to leverage real-time data streams from both our website and fleet of delivery trucks.

## Online Platform Optimization
We need to analyze clickstream data to understand customer preferences, enhance user experience, and optimize marketing strategies for key product categories such as mobile phones, laptops, and cameras.

### Clickstream Data Collected:
  * Item ID
  * Item Name
  * Click Count

## Fleet Management and Logistics Optimization
We must monitor and analyze __real-time telemetry data__ from our fleet of delivery trucks, utilizing IoT sensors installed in each vehicle. This data will enable us to optimize routes, reduce fuel consumption, proactively address maintenance issues, and ensure the safety and reliability of our delivery operations.

### Truck Telemetry Data Collected:
  * Truck ID: 3 unique truck IDs.
  * GPS Location: Latitude, Longitude, Altitude, Speed.
  * Vehicle Speed: Real-time speed of the vehicle.
  * Engine Diagnostics: Engine RPM, Fuel Level, Temperature, Oil Pressure, Battery Voltage.
  * Odometer Reading: Total distance traveled.
  * Fuel Consumption: Fuel usage over time
  * Vehicle Health and Maintenance: Brake status, Tire pressure, Transmission status
  * Environmental Conditions: Temperature, Humidity, Atmospheric Pressure.
[All data used here are random and simulated using the Python file trucks.py]

## Workflow

![Workflow Digram](https://github.com/Jayasenthur/E-Commerce-Telemetry-and-Clickstream-Data-Pipeline/blob/main/image.gif)

1. __Data Generation__:
    * Python scripts generate random __Clickstream Data__ (Item ID, Item Name, Click Count) and __Truck Telemetry Data__ (Truck ID, GPS Location, Engine Diagnostics, etc.).
    * Data is sent to Kinesis Data Streams (`ClickDataStream` and `TruckTelemetry`).
2. __Data Processing__:
    * Lambda Functions:
          * `KinesisToDynamoDBProcessor`: Processes Clickstream data and stores it in __DynamoDB__ (`ClickStreamData` table).
          * `TruckDataProcessor`: Processes Truck Telemetry data and stores it in __S3__ (`kinesis-telemetry-data-bucket/telemetry-data/`).
3. __Data Storage__:
    * __DynamoDB__: Stores Clickstream data for real-time analysis.
    * __S3__: Stores Truck Telemetry data as JSON files.
4. Data Ingestion into Snowflake:
    * __Firehose__: Loads Truck Telemetry data from Kinesis to S3.
    * __Snowpipe__: Automatically ingests data from S3 into Snowflake (`TRUCK_TELEMETRY_DATA` table) using SQS notifications.
5. __Data Visualization__:
    * Streamlit UI:
           * Fetches Clickstream data from DynamoDB.
           * Fetches Truck Telemetry data from Snowflake.
           * Displays data with visualizations for analysis.
6. __Historical Data Management__:
    * Snowflake table (`TRUCK_TELEMETRY_DATA`) uses __Type 2 Slowly Changing Dimensions (SCD)__ to maintain historical records of Truck Telemetry data.

## Schema for the Database

### 1. Clickstream Data (DynamoDB Table: `ClickStreamData`)

| Attribute       | Type      | Desription                   |
|-----------------|-----------|------------------------------|
| `Item_ID`         |   String  | Unique ID of the item clicked|
| `Timestamp`       |   String  | Timestamp of the click event |
| `Item_Name`       |   String  | Name of the item clicked     |
| `Click_Counts`    |   Number  | Number of clicks on the item |

### 2. Truck Telemetry Data (Snowflake Table: `TRUCK_TELEMETRY_DATA`)

The schema follows __Type 2 Slowly Changing Dimensions (SCD)__ to maintain historical data.

| Attribute                          | Type              | Description                                         |
|------------------------------------|-------------------|----------------------------------------------------|
| `TRUCK_ID`                         | STRING            | Unique ID of the truck.                            |
| `LOAD_TIMESTAMP`                   | TIMESTAMP_NTZ     | Timestamp when the data was loaded.               |
| `EFFECTIVE_START_DATE`             | TIMESTAMP_NTZ     | Start of the record's validity.                   |
| `EFFECTIVE_END_DATE`               | TIMESTAMP_NTZ     | End of the record's validity.                     |
| `IS_CURRENT`                       | BOOLEAN           | Indicates if this is the current record.          |
| `GPS_LATITUDE`                     | FLOAT             | Latitude of the truck's location.                 |
| `GPS_LONGITUDE`                    | FLOAT             | Longitude of the truck's location.                |
| `GPS_ALTITUDE`                     | FLOAT             | Altitude of the truck's location.                 |
| `GPS_SPEED`                        | FLOAT             | Speed of the truck.                               |
| `VEHICLE_SPEED`                    | FLOAT             | Speed of the vehicle.                             |
| `ENGINE_RPM`                       | FLOAT             | Engine RPM.                                       |
| `FUEL_LEVEL`                       | FLOAT             | Fuel level in the tank.                           |
| `ENGINE_TEMPERATURE`               | FLOAT             | Engine temperature.                               |
| `OIL_PRESSURE`                     | FLOAT             | Oil pressure.                                     |
| `BATTERY_VOLTAGE`                  | FLOAT             | Battery voltage.                                  |
| `ODOMETER_READING`                 | FLOAT             | Odometer reading.                                 |
| `FUEL_CONSUMPTION`                 | FLOAT             | Fuel consumption.                                 |
| `BRAKE_STATUS`                     | STRING            | Brake status.                                    |
| `TIRE_PRESSURE_FRONT_LEFT`         | FLOAT             | Front left tire pressure.                        |
| `TIRE_PRESSURE_FRONT_RIGHT`        | FLOAT             | Front right tire pressure.                       |
| `TIRE_PRESSURE_REAR_LEFT`          | FLOAT             | Rear left tire pressure.                         |
| `TIRE_PRESSURE_REAR_RIGHT`         | FLOAT             | Rear right tire pressure.                        |
| `TRANSMISSION_STATUS`              | STRING            | Transmission status.                             |
| `ENVIRONMENT_TEMPERATURE`          | FLOAT             | Environmental temperature.                        |
| `ENVIRONMENT_HUMIDITY`             | FLOAT             | Environmental humidity.                           |
| `ENVIRONMENT_PRESSURE`             | FLOAT             | Environmental pressure.                           |


      


      


