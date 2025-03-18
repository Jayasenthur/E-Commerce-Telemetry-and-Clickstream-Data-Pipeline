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


