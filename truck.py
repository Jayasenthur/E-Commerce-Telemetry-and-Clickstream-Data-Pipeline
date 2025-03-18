import boto3
import json
import random
import time
from datetime import datetime
import signal
import sys

# AWS Kinesis Configuration
kinesis_client = boto3.client('kinesis', region_name='us-east-1')  # Replace with your region
CLICK_STREAM_NAME = 'ClickDataStream'  # Replace with your Kinesis stream name
TRUCK_STREAM_NAME = 'TruckTelemetry'   # Replace with your Kinesis stream name

# Function to generate random ClickStream data
def generate_clickstream_data():
    items = [
        {"Item_ID": "MOB001", "Timestamp": datetime.utcnow().isoformat(), "Item_Name": "Mobile Phone", "Click_Counts": random.randint(100, 500)},
        {"Item_ID": "LAP002", "Timestamp": datetime.utcnow().isoformat(),"Item_Name": "Laptop", "Click_Counts": random.randint(50, 300)},
        {"Item_ID": "CAM003", "Timestamp": datetime.utcnow().isoformat(),"Item_Name": "Camera", "Click_Counts": random.randint(30, 200)}
    ]
    return random.choice(items)

# Function to generate random TruckTelemetry data
def generate_truck_telemetry_data():
    truck_id = random.choice(["TRK001", "TRK002", "TRK003"])
    telemetry_data = {
        "TRUCK_ID": truck_id,
        "LOAD_TIMESTAMP": datetime.utcnow().isoformat(),
        "EFFECTIVE_START_DATE": datetime.utcnow().isoformat(),
        "EFFECTIVE_END_DATE": None,  # NULL for current records
        "IS_CURRENT": True,  # TRUE for current records
        "GPS_LATITUDE": round(random.uniform(30.0, 40.0), 2),
        "GPS_LONGITUDE": round(random.uniform(-120.0, -80.0), 2),
        "GPS_ALTITUDE": round(random.uniform(0.0, 100.0), 2),
        "GPS_SPEED": round(random.uniform(40.0, 70.0), 2),
        "VEHICLE_SPEED": round(random.uniform(40.0, 70.0), 2),
        "ENGINE_RPM": random.randint(2000, 3000),
        "FUEL_LEVEL": round(random.uniform(50.0, 100.0), 2),
        "ENGINE_TEMPERATURE": round(random.uniform(80.0, 100.0), 2),
        "OIL_PRESSURE": round(random.uniform(30.0, 50.0), 2),
        "BATTERY_VOLTAGE": round(random.uniform(12.0, 14.5), 2),
        "ODOMETER_READING": round(random.uniform(80000.0, 120000.0), 2),
        "FUEL_CONSUMPTION": round(random.uniform(10.0, 20.0), 2),
        "BRAKE_STATUS": random.choice(["Good", "Needs Inspection"]),
        "TIRE_PRESSURE_FRONT_LEFT": round(random.uniform(30.0, 35.0), 2),
        "TIRE_PRESSURE_FRONT_RIGHT": round(random.uniform(30.0, 35.0), 2),
        "TIRE_PRESSURE_REAR_LEFT": round(random.uniform(33.0, 37.0), 2),
        "TIRE_PRESSURE_REAR_RIGHT": round(random.uniform(33.0, 37.0), 2),
        "TRANSMISSION_STATUS": random.choice(["Operational", "Needs Maintenance"]),
        "ENVIRONMENT_TEMPERATURE": round(random.uniform(10.0, 35.0), 2),
        "ENVIRONMENT_HUMIDITY": round(random.uniform(20.0, 80.0), 2),
        "ENVIRONMENT_PRESSURE": round(random.uniform(1000.0, 1020.0), 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    return telemetry_data

# Signal handler for keyboard interrupt
def signal_handler(sig, frame):
    print("\nKeyboard interrupt detected. Stopping the script gracefully...")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Main function to generate and send data
def main():
    while True:
        try:
            # Generate and send ClickStream data
            clickstream_data = generate_clickstream_data()
            click_response = send_to_kinesis(CLICK_STREAM_NAME, clickstream_data)
            print(f"Sent ClickStream Data: {clickstream_data} | Response: {click_response}")

            # Generate and send TruckTelemetry data
            truck_data = generate_truck_telemetry_data()
            truck_response = send_to_kinesis(TRUCK_STREAM_NAME, truck_data)
            print(f"Sent TruckTelemetry Data: {truck_data} | Response: {truck_response}")

            # Wait for 1 minute before sending the next batch of data
            print("Generating and sending data...")
            time.sleep(15)
        
       
        except KeyboardInterrupt:
            print("\nScript stopped by user.")

if __name__ == "__main__":
    main()