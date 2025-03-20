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

### 1. __Data Generation__:
* Python scripts generate random __Clickstream Data__ (Item ID, Item Name, Click Count) and __Truck Telemetry Data__ (Truck ID, GPS Location, Engine Diagnostics, etc.).
* Data is sent to Kinesis Data Streams (`ClickDataStream` and `TruckTelemetry`).
### 2. __Data Processing__:
* Lambda Functions:
   * `KinesisToDynamoDBProcessor`: Processes Clickstream data and stores it in __DynamoDB__ (`ClickStreamData` table).
   * `TruckDataProcessor`: Processes Truck Telemetry data and stores it in __S3__ (`kinesis-telemetry-data-bucket/telemetry-data/`).
### 3. __Data Storage__:
* __DynamoDB__: Stores Clickstream data for real-time analysis.
* __S3__: Stores Truck Telemetry data as JSON files.
### 4. Data Ingestion into Snowflake:
* __Firehose__: Loads Truck Telemetry data from Kinesis to S3.
* __Snowpipe__: Automatically ingests data from S3 into Snowflake (`TRUCK_TELEMETRY_DATA` table) using SQS notifications.
### 5. __Data Visualization__:
* Streamlit UI:
  * Fetches Clickstream data from DynamoDB.
  * Fetches Truck Telemetry data from Snowflake.
  * Displays data with visualizations for analysis.
### 6. __Historical Data Management__:
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

## Steps to Set Up the Project
### 1. Setting Up IAM Permissions for Lambda Functions
### KinesisToDynamoDBProcessor Lambda Function:
The function requires the following IAM permissions to interact with Kinesis and DynamoDB:
* __Kinesis__: `GetRecords`, `DescribeStream`, `ListShards` for ClickDataStream.
* __DynamoDB__: `PutItem` for ClickStreamData.
    
```python
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:GetRecords",
        "kinesis:DescribeStream",
        "kinesis:ListShards"
      ],
      "Resource": "arn:aws:kinesis:us-east-1:123456789012:stream/ClickDataStream"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/ClickStreamData"
    }
  ]
}
```
## Kinesis Trigger for Lambda Function
### KinesisToDynamoDBProcessor:
* Go to the __Lambda Console__.
* Add a trigger for the `ClickDataStream` Kinesis stream.
* Set the __Batch Size__ (e.g., 100) and __Batch Window__ (e.g., 60 seconds).

## Purpose of the Lambda Function KinesisToDynamoDBProcessor

The Lambda function KinesisToDynamoDBProcessor plays a critical role in real-time data pipeline. Its purpose is to process Clickstream data from the Kinesis Data Stream (`ClickDataStream`) and store it in the DynamoDB table (`ClickStreamData`).
1. __Real-Time Data Processing__:
   * The function is triggered whenever new records are added to the Kinesis Data Stream (ClickDataStream).
   * It processes the incoming Clickstream data in real time.
2. __Data Transformation__:
   * The function decodes the base64-encoded data from the Kinesis stream
   * It extracts relevant fields (e.g., Item_ID, Timestamp, Item_Name, Click_Counts) from the incoming records.
3. __Data Storage__:
   * The function writes the processed Clickstream data into the DynamoDB table (ClickStreamData).
   * Each record is stored as a new item in the DynamoDB table.
4. __Scalability and Reliability__:
   * The function is designed to handle large volumes of data efficiently.
   * It ensures that data is reliably stored in DynamoDB for further analysis and reporting.

### How It Works
1. __Trigger__:
    * The function is triggered by the Kinesis Data Stream (`ClickDataStream`) whenever new records are added.
2. __Data Processing__ :
    * The function processes each record in the Kinesis stream:
       * Decodes the base64-encoded data.
       * Parses the JSON payload to extract Clickstream data.
3. __Data validation__ : The function validates the data to ensure all required fields are present.
4. __Data Storage__:
    * The function inserts the processed data into the DynamoDB table (`ClickStreamData`) using the PutItem operation.
5. __Error Handling__:
    * The function includes error handling to ensure that any issues (e.g., invalid data, DynamoDB errors) are logged and do not disrupt the pipeline.                      |

 ### KinesisToDynamoDBProcessor Lamda code
 ```python
import json
import base64
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ClickStreamData')  # Ensure this matches your table name

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    for record in event['Records']:
        try:
            # Decode the base64-encoded Kinesis data
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data = json.loads(payload)
            logger.info(f"Processing record: {data}")

            # Validate the presence of required fields
            required_fields = ['Item_ID', 'Timestamp', 'Item_Name', 'Click_Counts']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                logger.error(f"Record is missing required fields: {missing_fields}. Data: {data}")
                continue  # Skip this record

            # Prepare the item for DynamoDB
            item = {
                'Timestamp': data['Timestamp'],  # Partition Key
                'Item_ID': data['Item_ID'],      # Sort Key
                'Item_Name': data['Item_Name'],
                'Click_Counts': data['Click_Counts']
            }
            logger.info(f"Prepared item for DynamoDB: {item}")

            # Insert data into DynamoDB
            table.put_item(Item=item)
            logger.info(f"Successfully inserted item: {item}")
        except Exception as e:
            logger.error(f"Error processing record: {e}")
    
    return {
        'statusCode': 200,
        'body': 'Processed {} records.'.format(len(event['Records']))
    }
```
## Code Explanation
### 1. Importing Libraries
```python
import json
import base64
import boto3
import logging
```
* `json`: Used to parse JSON data.
* `base64`: Used to decode base64-encoded data from Kinesis.
* `boto3`: AWS SDK for Python, used to interact with DynamoDB.
* `logging`: Used for logging messages (e.g., errors, debug information).

### 2. Configuring Logging
```python
logger = logging.getLogger()
logger.setLevel(logging.INFO)
```
* Sets up logging to log messages at the INFO level and above (e.g., INFO, ERROR).
  
### 3. Initializing DynamoDB Resource
```python
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ClickStreamData')
```
* Initializes a connection to the __DynamoDB__ service.
* Specifies the DynamoDB table (`ClickStreamData`) where the data will be stored.

### 4. Lambda Handler Function
```python
def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
```
* The `lambda_handler` is the entry point for the Lambda function.
* Logs the incoming event for debugging purposes.

### 5. Processing Kinesis Records
```python
for record in event['Records']:
    try:
        # Decode the base64-encoded Kinesis data
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        logger.info(f"Processing record: {data}")
```
* Iterates through each record in the Kinesis event.
* Decodes the base64-encoded data from Kinesis and parses it into a JSON object.

### 6. Validating Required Fields
```python
required_fields = ['Item_ID', 'Timestamp', 'Item_Name', 'Click_Counts']
missing_fields = [field for field in required_fields if field not in data]
if missing_fields:
    logger.error(f"Record is missing required fields: {missing_fields}. Data: {data}")
    continue  # Skip this record
```
* Checks if the incoming data contains all required fields (Item_ID, Timestamp, Item_Name, Click_Counts).
* If any fields are missing, logs an error and skips the record.

### 7. Preparing Data for DynamoDB
```python
item = {
    'Timestamp': data['Timestamp'],  # Partition Key
    'Item_ID': data['Item_ID'],      # Sort Key
    'Item_Name': data['Item_Name'],
    'Click_Counts': data['Click_Counts']
}
logger.info(f"Prepared item for DynamoDB: {item}")
```
* Prepares the data for insertion into DynamoDB by creating a dictionary (`item`) with the required fields.
* `Timestamp` is the __Partition Key__ and `Item_ID` is the __Sort Key__ in the DynamoDB table.

### 8. Inserting Data into DynamoDB
```python
table.put_item(Item=item)
logger.info(f"Successfully inserted item: {item}")
```
* Inserts the prepared item into the DynamoDB table using the put_item method.
* Logs a success message after the item is inserted.

### 9. Error Handling
```python
except Exception as e:
    logger.error(f"Error processing record: {e}")
```
* Catches and logs any exceptions that occur during processing (e.g., decoding errors, DynamoDB errors).

### 10. Returning a Response
```python
return {
    'statusCode': 200,
    'body': 'Processed {} records.'.format(len(event['Records']))
}
```
* Returns a response indicating the number of records processed.

### Example Input and Output
__Input (Kinesis Record)__:
```json
{
  "Item_ID": "MOB001",
  "Timestamp": "2025-03-17T15:35:54.597252",
  "Item_Name": "Mobile Phone",
  "Click_Counts": 289
}
```
__Output (DynamoDB Item)__:
The function writes the following item to the DynamoDB table:

| Attribute      | Value                           |
|----------------|---------------------------------|
| Item_ID        | "MOB001"                        |
| Timestamp      | "2025-03-17T15:35:54.597252"   |
| Item_Name      | "Mobile Phone"                  |
| Click_Counts   | 289      

## Purpose of Lamda function TruckDataProcessor 
The `TruckDataProcessor` Lambda function is designed to:
* Process real-time Truck Telemetry data from the Kinesis Data Stream (`TruckTelemetry`).
* Store the processed data in an __S3__ bucket (`kinesis-telemetry-data-bucket/telemetry-data/`) as JSON files.
* Enable further processing of the data (e.g., loading into `Snowflake` for analysis).

## IAM Permissions for the Lambda Function
The function requires the following IAM permissions to interact with Kinesis and S3:
```python
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:GetRecords",
        "kinesis:DescribeStream",
        "kinesis:ListShards"
      ],
      "Resource": "arn:aws:kinesis:us-east-1:123456789012:stream/TruckTelemetry"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::kinesis-telemetry-data-bucket/telemetry-data/*"
    }
  ]
}
```
## Explanation of Permissions
## Kinesis Permissions:
* `GetRecords`: To read records from the Kinesis stream.
* `DescribeStream`: To get details about the Kinesis stream.
* `ListShards`: To list shards in the Kinesis stream.
## S3 Permissions:
* `PutObject`: To upload JSON files to the S3 bucket.

## Kinesis Trigger for Lambda Function
The `TruckDataProcessor` function is triggered by the Kinesis Data Stream (`TruckTelemetry`). Here’s how the trigger is configured:

* Kinesis Stream: `TruckTelemetry`.
* Batch Size: Number of records to process in a single invocation (e.g., 100).
* Batch Window: Maximum time to wait before invoking the function (e.g., 60 seconds).

## How the Lambda Function Works
__Trigger__:
The function is triggered whenever new records are added to the Kinesis Data Stream (`TruckTelemetry`).

__Data Processing__:
* The function processes each record in the Kinesis stream:
    * Decodes the base64-encoded data.
    * Parses the JSON payload to extract Truck Telemetry data.
      
__Data Storage__:
* The function generates a unique file name using a timestamp.
* Uploads the processed data as a JSON file to the S3 bucket (`kinesis-telemetry-data-bucket/telemetry-data/`).

__Error Handling__:
The function includes error handling to ensure that any issues (e.g., invalid data, S3 errors) are logged and do not disrupt the pipeline.

## Lambda Code Explanation
### 1. Importing Libraries
```python
import json
import boto3
import base64
from datetime import datetime
```
* `json`: Used to parse JSON data.
* `boto3`: AWS SDK for Python, used to interact with S3.
* `base64`: Used to decode base64-encoded data from Kinesis.
* `datetime`: Used to generate timestamps for file names.

### 2. Initializing S3 Client
```python
s3_client = boto3.client('s3')
S3_BUCKET_NAME = 'kinesis-telemetry-data-bucket'
S3_FOLDER_NAME = 'telemetry-data/'
```
* Initializes a connection to the S3 service.
* Specifies the S3 bucket and folder where the data will be stored.

### 3. Lambda Handler Function
```python
def lambda_handler(event, context):
    try:
        # Check if 'Records' key exists in the event
        if 'Records' not in event:
            raise KeyError("'Records' key not found in the event. Ensure the event is from a Kinesis stream.")
        
        print(f"Number of records received: {len(event['Records'])}")
```
* The `lambda_handler` is the entry point for the Lambda function.
* Checks if the event contains the `Records` key (to ensure it’s from a Kinesis stream).

### 4. Processing Kinesis Records
```python
for record in event['Records']:
    # Kinesis data is base64 encoded, so decode it
    payload = base64.b64decode(record['kinesis']['data'])
    telemetry_data = json.loads(payload)
    
    # Log the decoded data for debugging
    print(f"Decoded telemetry data: {telemetry_data}")
```
* Iterates through each record in the Kinesis event.
* Decodes the base64-encoded data from Kinesis and parses it into a JSON object.

### 5. Generating a Unique File Name
```python
file_name = f"{S3_FOLDER_NAME}{datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}.json"
```
* Generates a unique file name using the current timestamp (e.g., telemetry-data/2025-03-17-15-35-54-597252.json).

### 6. Uploading Data to S3
```python
s3_client.put_object(
    Bucket=S3_BUCKET_NAME,
    Key=file_name,
    Body=json.dumps(telemetry_data))
    
print(f"Successfully stored telemetry data in S3: {file_name}")
```
* Uploads the processed data as a JSON file to the S3 bucket.

### 7. Error Handling
```python
except KeyError as e:
    print(f"KeyError: {str(e)}")
    return {
        'statusCode': 400,
        'body': json.dumps(f"Error: {str(e)}")
    }
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    return {
        'statusCode': 500,
        'body': json.dumps(f"Error: {str(e)}")
    }
```
* Catches and logs any exceptions that occur during processing (e.g., decoding errors, S3 errors).

### 8. Returning a Response
```python
return {
    'statusCode': 200,
    'body': json.dumps('Telemetry data stored in S3 successfully!')
}
```
* Returns a response indicating success.

### Example Input and Output
#### Input (Kinesis Event):
```json
{
  "Records": [
    {
      "kinesis": {
        "data": "eyJ0cnVja19pZCI6ICJUUkswMDEiLCJnYW1lX2xvY2F0aW9uIjogeyJsYXRpdHVkZSI6IDM0LjA1MjMsImxvbmdpdHVkZSI6IC0xMTguMjU2N30sInZlaGljbGVfc3BlZWQiOiA2NS4wLCJlbmdpbmVfZGlhZ25vc3RpY3MiOiB7ImVuZ2luZV9ycG0iOiAyNTAwLCJmdWVsX2xldmVsIjogNzguNSwiZW5naW5lX3RlbXBlcmF0dXJlIjogMTg5LjN9LCJvZG9tZXRlcl9yZWFkaW5nIjogODAwMDAuMCwiZnVlbF9jb25zdW1wdGlvbiI6IDEwLjAsInZlaGljbGVfaGVhbHRoX2FuZF9tYWludGVuYW5jZSI6IHsiYnJha2Vfc3RhdHVzIjogIkdvb2QiLCJ0aXJlX3ByZXNzdXJlIjogeyJmcm9udF9sZWZ0IjogMzIuMCwiZnJvbnRfcmlnaHQiOiAzMi4wLCJyZWFyX2xlZnQiOiAzNS4wLCJyZWFyX3JpZ2h0IjogMzUuMH0sInRyYW5zbWlzc2lvbl9zdGF0dXMiOiAiT3BlcmF0aW9uYWwifSwiZW52aXJvbm1lbnRhbF9jb25kaXRpb25zIjogeyJ0ZW1wZXJhdHVyZSI6IDIyLjAsImh1bWlkaXR5IjogNTQuMCwiYXRtb3NwaGVyaWNfcHJlc3N1cmUiOiAxMDEzLjI1fSwidGltZXN0YW1wIjogIjIwMjUtMDMtMTdUMTU6MzU6NTQuNTk3MjUyIn0="
      }
    }
  ]
}
```
Decoded Data:
```json
{
  "truck_id": "TRK001",
  "gps_location": {
    "latitude": 34.0523,
    "longitude": -118.2567
  },
  "vehicle_speed": 65.0,
  "engine_diagnostics": {
    "engine_rpm": 2500,
    "fuel_level": 78.5,
    "engine_temperature": 189.3
  },
  "odometer_reading": 80000.0,
  "fuel_consumption": 10.0,
  "vehicle_health_and_maintenance": {
    "brake_status": "Good",
    "tire_pressure": {
      "front_left": 32.0,
      "front_right": 32.0,
      "rear_left": 35.0,
      "rear_right": 35.0
    },
    "transmission_status": "Operational"
  },
  "environmental_conditions": {
    "temperature": 22.0,
    "humidity": 54.0,
    "atmospheric_pressure": 1013.25
  },
  "timestamp": "2025-03-17T15:35:54.597252"
}
```
### Output (S3 File):
The function uploads the above JSON data to the S3 bucket with a unique file name, e.g., `telemetry-data/2025-03-17-15-35-54-597252.json`.

### Steps to Create an S3 Bucket and Enable Notifications
## 1. Create an S3 Bucket
   1. Go to the S3 Console:
        * Open the AWS S3 Console.
   2. Create a New Bucket:
        * Click Create bucket.
        * Enter a Bucket name (e.g., `kinesis-telemetry-data-bucket`).
        * Choose the Region (e.g., `us-east-1`).
        * Leave other settings as default (or configure as needed).
        * Click Create bucket.
## 2.  Enable Event Notifications
   1. Go to the Bucket Properties:
        * In the S3 Console, select the bucket you created (`kinesis-telemetry-data-bucket`).
        * Go to the __Properties__ tab.
   2. Enable Event Notifications:
        * Scroll down to the __Event notifications section__.
        * Click __Create event notification__.
   3. Configure Event Notification:
        * Event name: `snowflake-auto-ingest` (or any name you prefer).
        * Event types: Select `All object create events`.
        * Prefix: `telemetry-data/` (to filter events for the specific folder).
        * Send to: Choose __SQS Queue__.
        * SQS Queue: Select the SQS queue created by Snowflake (e.g., `arn:aws:sqs:us-east-1:123456789012:sf-snowpipe-queue`).
   4. Save the Configuration:
        * Click Save changes.
           


