from fastapi import FastAPI
import hashlib
import os
from datetime import datetime

app = FastAPI()

# File names
FIRMWARE_FILE = "firmware.bin"
SIGNATURE_FILE = "firmware.sig"

# Firmware details
firmware_info = {
    "version": "1.0.0",
    "release_date": str(datetime.now()),
    "hash": "",
    "signature_file": SIGNATURE_FILE
}

# Security logs
security_logs = []


# Generate SHA-256 hash
def generate_hash(filename):

    if not os.path.exists(filename):
        return None

    with open(filename, "rb") as f:
        data = f.read()

    return hashlib.sha256(data).hexdigest()


# Home page
@app.get("/")
def home():
    return {
        "status": "Secure OTA Server Running"
    }


# Check latest firmware
@app.get("/firmware/latest")
def get_latest_firmware():

    firmware_hash = generate_hash(FIRMWARE_FILE)

    if firmware_hash is None:
        return {
            "error": "Firmware file not found"
        }

    firmware_info["hash"] = firmware_hash

    return {
        "message": "Latest firmware available",
        "firmware": firmware_info
    }


# Download firmware information
@app.get("/firmware/download")
def download_firmware():

    if not os.path.exists(FIRMWARE_FILE):
        return {
            "error": "Firmware file not found"
        }

    return {
        "firmware_file": FIRMWARE_FILE,
        "signature_file": SIGNATURE_FILE,
        "hash": generate_hash(FIRMWARE_FILE)
    }


# Add security event logs
@app.post("/security/log")
def add_security_log(data: dict):

    log = {
        "timestamp": str(datetime.now()),
        "device_id": data.get("device_id"),
        "event": data.get("event"),
        "status": data.get("status")
    }

    security_logs.append(log)

    return {
        "message": "Security log stored successfully",
        "log": log
    }


# View all security logs
@app.get("/security/logs")
def get_logs():
    return security_logs