import os
import psutil
import time
import pandas as pd
from datetime import datetime
from minio import Minio

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Create folders
data_dir = os.path.join(base_dir, "data")
logs_dir = os.path.join(base_dir, "logs")

os.makedirs(data_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)

# File paths
file_path = os.path.join(data_dir, "resource_metrics.csv")
log_file = os.path.join(logs_dir, "system_logs.txt")

# Create CSV if not exists
if not os.path.exists(file_path):
    pd.DataFrame(
        columns=["timestamp", "cpu", "ram", "disk"]
    ).to_csv(file_path, index=False)

# MinIO setup
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)

bucket_name = "cloud-monitoring-data"

if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

print("🚀 Monitoring Started...\n")

# Main loop
while True:
    try:
        # Collect metrics
        metrics = {
            "timestamp": str(datetime.now()),
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent
        }

        # Print to terminal
        print(metrics)

        # Save to CSV
        pd.DataFrame([metrics]).to_csv(
            file_path,
            mode="a",
            header=False,
            index=False
        )

        # Upload to MinIO
        client.fput_object(
            bucket_name,
            "resource_metrics.csv",
            file_path
        )

        print("✔ Uploaded to MinIO successfully\n")

        # Save to logs
        with open(log_file, "a") as f:
            f.write(f"{metrics} | Uploaded to MinIO\n")

    except Exception as e:
        print("❌ Error:", e)

        # Log errors
        with open(log_file, "a") as f:
            f.write(f"ERROR: {e}\n")

    # Wait 5 seconds
    time.sleep(5)